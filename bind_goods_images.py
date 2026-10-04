"""
从百度图片搜索按商品标题查图，下载并绑定到 Goods.cover_image。
"""
import os
import re
import sys
import ssl
import json
import time
import random
import http.cookiejar
import urllib.parse
import urllib.request
from io import BytesIO

# Windows 控制台默认 GBK，会撞非 ASCII 输出；强制 UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_hand_market.settings')
django.setup()

from django.core.files.base import ContentFile  # noqa: E402
from PIL import Image  # noqa: E402

from goods.models import Goods  # noqa: E402


# 每个商品对应的搜索关键词（更精准）
QUERY_MAP = {
    'iPhone 13 Pro 二手 95新': 'iPhone 13 Pro 手机',
    'MacBook Pro 16寸 2021': 'MacBook Pro 16寸 笔记本',
    'Nike Air Max 运动鞋 42码': 'Nike Air Max 运动鞋',
    '优衣库羽绒服 男款 L码': '优衣库 男款 羽绒服',
    '小米空气净化器 Pro H': '小米空气净化器 Pro H',
    '宜家马尔姆双人床 1.8米': '宜家 马尔姆 双人床',
    'Python编程从入门到实践': 'Python编程从入门到实践 书',
    '考研英语历年真题解析': '考研英语 真题 书',
    '迪卡侬登山背包 30L': '迪卡侬 登山背包',
    '瑜伽垫 防滑加厚': '瑜伽垫 紫色',
    '婴儿推车 可坐可躺': '婴儿推车 高景观',
    '贝亲奶瓶 160ml + 240ml': '贝亲 奶瓶',
}

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

_SSL = ssl.create_default_context()
_SSL.check_hostname = False
_SSL.verify_mode = ssl.CERT_NONE


def build_opener():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj),
        urllib.request.HTTPSHandler(context=_SSL),
    )
    opener.addheaders = [
        ('User-Agent', UA),
        ('Accept-Language', 'zh-CN,zh;q=0.9'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
    ]
    # 预热：拿 Cookie
    try:
        opener.open('https://image.baidu.com/', timeout=15).read()
    except Exception as e:
        print(f'  警告：预热首页失败 {e}')
    return opener


def baidu_search_images(opener, keyword, max_results=30):
    """调用百度图片 acjson 接口，返回可下载 URL 列表。"""
    # 每次搜索前访问一次搜索结果页，刷新 Referer 匹配
    idx_url = 'https://image.baidu.com/search/index?tn=baiduimage&word=' + urllib.parse.quote(keyword)
    try:
        opener.open(idx_url, timeout=15).read()
    except Exception:
        pass

    urls = []
    for pn in (0, 30, 60):
        params = {
            'tn': 'resultjson_com',
            'logid': str(random.randint(10 ** 15, 10 ** 16 - 1)),
            'ipn': 'rj',
            'ct': '201326592',
            'fp': 'result',
            'queryWord': keyword,
            'cl': '2',
            'lm': '-1',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'st': '-1',
            'word': keyword,
            'face': '0',
            'istype': '2',
            'nc': '1',
            'pn': str(pn),
            'rn': '30',
        }
        url = 'https://image.baidu.com/search/acjson?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={'Referer': idx_url})
        try:
            raw = opener.open(req, timeout=15).read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f'    搜索请求失败 pn={pn}: {e}')
            continue
        raw = re.sub(r'[\x00-\x1f\x7f]', ' ', raw)
        try:
            j = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for item in j.get('data', []) or []:
            if not item:
                continue
            for key in ('thumbURL', 'middleURL', 'hoverURL'):
                v = item.get(key)
                if v and v.startswith('http'):
                    urls.append(v)
                    break
            if len(urls) >= max_results:
                return urls
    return urls


def try_download_image(opener, candidate_urls):
    """依次尝试下载，返回 (PIL.Image, 原始URL) 或 (None, None)。"""
    for u in candidate_urls:
        try:
            req = urllib.request.Request(u, headers={'Referer': 'https://image.baidu.com/'})
            data = opener.open(req, timeout=10).read()
            if len(data) < 3 * 1024:
                continue
            img = Image.open(BytesIO(data))
            img.load()
            if img.width < 200 or img.height < 200:
                continue
            return img, u
        except Exception:
            continue
    return None, None


def save_cover(goods, pil_img):
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    max_side = 800
    w, h = pil_img.size
    scale = min(1.0, max_side / max(w, h))
    if scale < 1.0:
        pil_img = pil_img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    buf = BytesIO()
    pil_img.save(buf, 'JPEG', quality=85, optimize=True)
    filename = f'goods_{goods.id}.jpg'
    goods.cover_image.save(filename, ContentFile(buf.getvalue()), save=True)


def main():
    goods_qs = Goods.objects.all().order_by('id')
    total = goods_qs.count()
    print(f'共 {total} 件商品待处理\n')

    opener = build_opener()

    ok, fail = 0, 0
    for goods in goods_qs:
        query = QUERY_MAP.get(goods.title, goods.title)
        print(f'[{goods.id}] {goods.title}  <-  搜索: {query}')
        try:
            urls = baidu_search_images(opener, query)
        except Exception as e:
            print(f'    搜索异常: {e}')
            urls = []
        print(f'    候选 {len(urls)} 张')
        img, used_url = try_download_image(opener, urls)
        if img is None:
            print(f'    [FAIL] 未能下载到可用图片')
            fail += 1
            continue
        save_cover(goods, img)
        print(f'    [OK]   已绑定 {goods.cover_image.name}  (源: {used_url[:80]}...)')
        ok += 1
        time.sleep(0.4)

    print(f'\n完成：成功 {ok} / 失败 {fail} / 总计 {total}')


if __name__ == '__main__':
    main()
