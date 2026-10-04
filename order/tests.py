"""订单模块测试。

覆盖：
- Order 模型：字符串表示、默认状态、订单号唯一约束
- 订单列表视图：登录保护、只展示当前买家订单
- 订单详情视图：登录保护、他人订单返回 404
"""
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase, override_settings
from django.urls import reverse

from goods.models import Goods
from order.models import Order

# 将测试期间上传的文件隔离到临时目录
TEST_MEDIA_ROOT = tempfile.mkdtemp()


def make_image(name='cover.jpg'):
    return SimpleUploadedFile(name, b'fake-image-content', content_type='image/jpeg')


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class OrderModelTest(TestCase):
    """Order 模型单元测试。"""

    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='pass12345')
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.goods = Goods.objects.create(
            seller=self.seller, title='商品', description='描述', price=100, cover_image=make_image(),
        )

    def _make_order(self, order_no='202601010001'):
        return Order.objects.create(
            order_no=order_no,
            buyer=self.buyer,
            seller=self.seller,
            goods=self.goods,
            price=100,
            address='北京市朝阳区',
        )

    def test_str_returns_order_no(self):
        order = self._make_order()
        self.assertEqual(str(order), '202601010001')

    def test_default_status_is_pending(self):
        order = self._make_order()
        self.assertEqual(order.status, 'pending')

    def test_order_no_unique_constraint(self):
        self._make_order(order_no='DUP001')
        with self.assertRaises(IntegrityError):
            self._make_order(order_no='DUP001')


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class OrderListViewTest(TestCase):
    """订单列表视图测试。"""

    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.goods = Goods.objects.create(
            seller=self.seller, title='商品', description='描述', price=100, cover_image=make_image(),
        )

    def _make_order(self, order_no, buyer):
        return Order.objects.create(
            order_no=order_no, buyer=buyer, seller=self.seller, goods=self.goods, price=100, address='北京市',
        )

    def test_order_list_requires_login(self):
        response = self.client.get(reverse('order:list'))
        self.assertEqual(response.status_code, 302)

    def test_shows_only_current_buyers_orders(self):
        self._make_order('A001', self.buyer)
        self._make_order('A002', self.other)
        self.client.login(username='buyer', password='pass12345')
        response = self.client.get(reverse('order:list'))
        order_nos = [order.order_no for order in response.context['orders']]
        self.assertIn('A001', order_nos)
        self.assertNotIn('A002', order_nos)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class OrderDetailViewTest(TestCase):
    """订单详情视图测试。"""

    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.goods = Goods.objects.create(
            seller=self.seller, title='商品', description='描述', price=100, cover_image=make_image(),
        )
        self.order = Order.objects.create(
            order_no='A001', buyer=self.buyer, seller=self.seller, goods=self.goods, price=100, address='北京市',
        )

    def test_detail_requires_login(self):
        response = self.client.get(reverse('order:detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)

    def test_detail_own_order_returns_200(self):
        self.client.login(username='buyer', password='pass12345')
        response = self.client.get(reverse('order:detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)

    def test_detail_other_users_order_returns_404(self):
        self.client.login(username='other', password='pass12345')
        response = self.client.get(reverse('order:detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 404)
