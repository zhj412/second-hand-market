"""首页视图测试。

覆盖项目首页（home）的核心功能：
- 首页可正常访问
- 首页只展示「在售」状态的商品
- 首页展示启用的顶级分类
"""
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from goods.models import Category, Goods

# 将测试期间上传的文件隔离到临时目录，避免污染真实的 media/ 目录
TEST_MEDIA_ROOT = tempfile.mkdtemp()


def make_image(name='cover.jpg'):
    """构造一个简单的测试图片文件对象。"""
    return SimpleUploadedFile(name, b'fake-image-content', content_type='image/jpeg')


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class HomeViewTest(TestCase):
    """首页视图测试。"""

    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.category = Category.objects.create(name='数码产品')

    def _make_goods(self, title, status='on_sale'):
        return Goods.objects.create(
            seller=self.seller,
            category=self.category,
            title=title,
            description='测试描述',
            price=100,
            status=status,
            cover_image=make_image(),
        )

    def test_home_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_only_shows_on_sale_goods(self):
        self._make_goods('在售商品', status='on_sale')
        self._make_goods('已售商品', status='sold')
        self._make_goods('下架商品', status='off_sold')
        response = self.client.get(reverse('home'))
        titles = [goods.title for goods in response.context['goods_list']]
        self.assertIn('在售商品', titles)
        self.assertNotIn('已售商品', titles)
        self.assertNotIn('下架商品', titles)

    def test_home_shows_active_top_level_categories(self):
        response = self.client.get(reverse('home'))
        category_names = [category.name for category in response.context['categories']]
        self.assertIn('数码产品', category_names)
