import os
import django
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_hand_market.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from goods.models import Goods, Category
from cart.models import Cart
from order.models import Order
from favorite.models import Favorite
from message.models import Message

def run():
    print("=" * 50)
    print("开始导入二手交易平台测试数据...")
    print("=" * 50)

    # 1. 创建测试用户
    print("\n[1/6] 创建测试用户...")
    users_data = ['小明', '小红', '张三', '李四', '王五']
    users = []
    for i, name in enumerate(users_data):
        user, created = User.objects.get_or_create(
            username=f'user{i+1}',
            defaults={'email': f'user{i+1}@example.com'}
        )
        if created:
            user.set_password('123456')
            user.save()
            UserProfile.objects.create(
                user=user,
                nickname=name,
                phone=f'138{str(random.randint(10000000, 99999999))}',
                address='北京市朝阳区某某街道123号'
            )
            print(f"  创建用户: {name} (user{i+1}/123456)")
        users.append(user)

    # 2. 创建商品分类（已提前创建，这里确保存在）
    print("\n[2/6] 确保商品分类存在...")
    categories_data = ['数码产品', '服饰鞋包', '家居生活', '图书文具', '运动户外', '母婴用品']
    categories = []
    for name in categories_data:
        cat, created = Category.objects.get_or_create(name=name, defaults={'sort': 0})
        categories.append(cat)
        print(f"  {'创建' if created else '已存在'}分类: {name}")

    # 3. 创建测试商品
    print("\n[3/6] 创建测试商品...")
    goods_templates = [
        ('iPhone 13 Pro 二手 95新', '数码产品', 4599, 6999, 'iPhone 13 Pro 256GB，外观完好，功能正常，电池健康85%'),
        ('MacBook Pro 16寸 2021', '数码产品', 12999, 18999, 'M1 Pro芯片，16G内存，512G固态，带原装充电器'),
        ('Nike Air Max 运动鞋 42码', '服饰鞋包', 399, 799, '9成新，仅穿过几次，原盒包装'),
        ('优衣库羽绒服 男款 L码', '服饰鞋包', 299, 599, '黑色，轻薄保暖，穿过一个冬季'),
        ('小米空气净化器 Pro H', '家居生活', 599, 1299, '使用半年，功能完好，滤芯剩余50%'),
        ('宜家马尔姆双人床 1.8米', '家居生活', 800, 1999, '9成新，白色，需自提'),
        ('Python编程从入门到实践', '图书文具', 39, 89, '几乎全新，无笔记划痕'),
        ('考研英语历年真题解析', '图书文具', 25, 58, '2023版，部分题已做'),
        ('迪卡侬登山背包 30L', '运动户外', 129, 299, '蓝色，防水材质，仅用过一次'),
        ('瑜伽垫 防滑加厚', '运动户外', 49, 99, '紫色，10mm厚，附带收纳袋'),
        ('婴儿推车 可坐可躺', '母婴用品', 399, 899, '9成新，宝宝大了用不上了，功能完好'),
        ('贝亲奶瓶 160ml + 240ml', '母婴用品', 89, 158, '几乎全新，仅消毒未使用，带原装奶嘴'),
    ]
    
    goods_list = []
    for i, (title, cat_name, price, original_price, desc) in enumerate(goods_templates):
        category = next(c for c in categories if c.name == cat_name)
        seller = random.choice(users)
        goods, created = Goods.objects.get_or_create(
            title=title,
            defaults={
                'seller': seller,
                'category': category,
                'price': price,
                'original_price': original_price,
                'description': desc,
                'status': 'on_sale',
                'view_count': random.randint(10, 200),
            }
        )
        if created:
            print(f"  创建商品: {title}")
        goods_list.append(goods)

    # 4. 创建购物车数据
    print("\n[4/6] 创建购物车数据...")
    for user in users[:3]:
        for goods in random.sample(goods_list, 2):
            Cart.objects.get_or_create(user=user, goods=goods)
    print(f"  创建了购物车记录")

    # 5. 创建收藏数据
    print("\n[5/6] 创建收藏数据...")
    for user in users:
        for goods in random.sample(goods_list, random.randint(1, 3)):
            Favorite.objects.get_or_create(user=user, goods=goods)
    print(f"  创建了收藏记录")

    # 6. 创建消息数据
    print("\n[6/6] 创建消息数据...")
    for i, sender in enumerate(users[:2]):
        receiver = users[i+2]
        Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=f"你好，请问{random.choice(goods_list).title}还能优惠吗？",
            is_read=random.choice([True, False])
        )
    print(f"  创建了消息记录")

    print("\n" + "=" * 50)
    print("测试数据导入完成！")
    print("=" * 50)
    print(f"\n统计信息：")
    print(f"  用户: {User.objects.count()} 个（含 admin）")
    print(f"  分类: {Category.objects.count()} 个")
    print(f"  商品: {Goods.objects.count()} 件")
    print(f"  购物车: {Cart.objects.count()} 条")
    print(f"  收藏: {Favorite.objects.count()} 条")
    print(f"  消息: {Message.objects.count()} 条")
    print(f"\n测试账号：")
    print(f"  管理员: admin / admin123")
    print(f"  普通用户: user1 / 123456")
    print(f"  普通用户: user2 / 123456")

if __name__ == '__main__':
    run()
