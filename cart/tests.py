"""购物车模块测试。

覆盖：
- Cart 模型：字符串表示、默认数量、用户-商品唯一约束
- 购物车视图：登录保护、只展示当前用户的购物车
"""
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase, override_settings
from django.urls import reverse

from cart.models import Cart
from goods.models import Goods

# 将测试期间上传的文件隔离到临时目录
TEST_MEDIA_ROOT = tempfile.mkdtemp()


def make_image(name='cover.jpg'):
    return SimpleUploadedFile(name, b'fake-image-content', content_type='image/jpeg')


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class CartModelTest(TestCase):
    """Cart 模型单元测试。"""

    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.goods = Goods.objects.create(
            seller=self.seller, title='商品', description='描述', price=100, cover_image=make_image(),
        )

    def test_str_contains_user_and_goods(self):
        cart = Cart.objects.create(user=self.user, goods=self.goods)
        self.assertEqual(str(cart), 'u1 - 商品')

    def test_default_quantity_is_one(self):
        cart = Cart.objects.create(user=self.user, goods=self.goods)
        self.assertEqual(cart.quantity, 1)

    def test_unique_constraint_on_user_and_goods(self):
        Cart.objects.create(user=self.user, goods=self.goods)
        with self.assertRaises(IntegrityError):
            Cart.objects.create(user=self.user, goods=self.goods)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class CartListViewTest(TestCase):
    """购物车列表视图测试。"""

    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.other = User.objects.create_user(username='u2', password='pass12345')
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.goods1 = Goods.objects.create(
            seller=self.seller, title='商品1', description='描述', price=100, cover_image=make_image(),
        )
        self.goods2 = Goods.objects.create(
            seller=self.seller, title='商品2', description='描述', price=200, cover_image=make_image(),
        )

    def test_cart_requires_login(self):
        response = self.client.get(reverse('cart:list'))
        self.assertEqual(response.status_code, 302)

    def test_shows_only_current_users_items(self):
        Cart.objects.create(user=self.user, goods=self.goods1)
        Cart.objects.create(user=self.other, goods=self.goods2)
        self.client.login(username='u1', password='pass12345')
        response = self.client.get(reverse('cart:list'))
        titles = [item.goods.title for item in response.context['cart_items']]
        self.assertIn('商品1', titles)
        self.assertNotIn('商品2', titles)
