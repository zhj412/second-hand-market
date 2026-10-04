"""接口自动化测试（DRF APITestCase）。

覆盖：
- 商品接口：列表只返回在售、搜索、详情、404、创建（需登录）
- 分类接口：列表只返回启用分类
- 注册接口：成功返回 Token、密码不一致、用户名重复
- 登录接口：获取 Token、密码错误
- 鉴权与数据隔离：匿名访问受保护接口返回 401，Token 认证后只返回自己的数据
"""
import base64
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cart.models import Cart
from favorite.models import Favorite
from goods.models import Category, Goods
from message.models import Message
from order.models import Order

TEST_MEDIA_ROOT = tempfile.mkdtemp()


# 1x1 透明 PNG，真实有效图片（DRF 的 ImageField 会校验图片内容有效性）
_VALID_PNG = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
)


def make_image(name='cover.png'):
    return SimpleUploadedFile(name, _VALID_PNG, content_type='image/png')


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class GoodsAPITest(APITestCase):
    """商品接口测试。"""

    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.category = Category.objects.create(name='数码产品')
        self.goods = Goods.objects.create(
            seller=self.seller, category=self.category, title='iPhone 13',
            description='95新', price=4599, cover_image=make_image(), status='on_sale',
        )
        Goods.objects.create(
            seller=self.seller, category=self.category, title='已售商品',
            description='x', price=100, cover_image=make_image(), status='sold',
        )

    def test_list_only_on_sale(self):
        response = self.client.get('/api/goods/')
        self.assertEqual(response.status_code, 200)
        titles = [item['title'] for item in response.data]
        self.assertIn('iPhone 13', titles)
        self.assertNotIn('已售商品', titles)

    def test_list_search(self):
        response = self.client.get('/api/goods/', {'q': 'iPhone'})
        titles = [item['title'] for item in response.data]
        self.assertIn('iPhone 13', titles)
        self.assertNotIn('已售商品', titles)

    def test_list_filter_by_category(self):
        other_category = Category.objects.create(name='图书')
        Goods.objects.create(
            seller=self.seller, category=other_category, title='Python 书',
            description='x', price=50, cover_image=make_image(), status='on_sale',
        )
        response = self.client.get('/api/goods/', {'category': self.category.pk})
        titles = [item['title'] for item in response.data]
        self.assertIn('iPhone 13', titles)
        self.assertNotIn('Python 书', titles)

    def test_detail(self):
        response = self.client.get(f'/api/goods/{self.goods.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'iPhone 13')
        self.assertEqual(response.data['seller_name'], 'seller')

    def test_detail_404(self):
        response = self.client.get('/api/goods/99999/')
        self.assertEqual(response.status_code, 404)

    def test_create_requires_auth(self):
        response = self.client.post('/api/goods/', {
            'title': '新商品', 'description': 'd', 'price': 10, 'category': self.category.pk,
        })
        self.assertEqual(response.status_code, 401)

    def test_create_success_with_auth(self):
        token, _ = Token.objects.get_or_create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post('/api/goods/', {
            'title': '新商品', 'description': '描述', 'price': '10.00',
            'category': self.category.pk, 'cover_image': make_image('new.jpg'),
        }, format='multipart')
        self.assertEqual(response.status_code, 201)
        goods = Goods.objects.get(title='新商品')
        self.assertEqual(goods.seller, self.seller)


class CategoryAPITest(APITestCase):
    """分类接口测试。"""

    def test_list_only_active_categories(self):
        Category.objects.create(name='数码产品')
        Category.objects.create(name='图书', is_active=False)
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        names = [c['name'] for c in response.data]
        self.assertIn('数码产品', names)
        self.assertNotIn('图书', names)


class AuthAPITest(APITestCase):
    """注册与登录接口测试。"""

    def test_register_success_returns_token(self):
        response = self.client.post('/api/register/', {
            'username': 'newuser', 'password': 'abc12345', 'password2': 'abc12345', 'phone': '13800138000',
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        response = self.client.post('/api/register/', {
            'username': 'newuser', 'password': 'abc12345', 'password2': 'different',
        })
        self.assertEqual(response.status_code, 400)

    def test_register_duplicate_username(self):
        User.objects.create_user(username='taken', password='abc12345')
        response = self.client.post('/api/register/', {
            'username': 'taken', 'password': 'abc12345', 'password2': 'abc12345',
        })
        self.assertEqual(response.status_code, 400)

    def test_login_obtain_token(self):
        User.objects.create_user(username='alice', password='pass12345')
        response = self.client.post('/api/login/', {'username': 'alice', 'password': 'pass12345'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_wrong_password(self):
        User.objects.create_user(username='alice', password='pass12345')
        response = self.client.post('/api/login/', {'username': 'alice', 'password': 'wrong'})
        self.assertEqual(response.status_code, 400)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProtectedAPITest(APITestCase):
    """受保护接口（订单/收藏/购物车/消息）的鉴权与数据隔离测试。"""

    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.category = Category.objects.create(name='数码产品')
        self.goods1 = Goods.objects.create(
            seller=self.seller, category=self.category, title='商品1',
            description='d', price=100, cover_image=make_image(),
        )
        self.goods2 = Goods.objects.create(
            seller=self.seller, category=self.category, title='商品2',
            description='d', price=200, cover_image=make_image(),
        )
        self.token, _ = Token.objects.get_or_create(user=self.buyer)

    def test_orders_requires_auth(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 401)

    def test_orders_only_own_with_token(self):
        Order.objects.create(order_no='A001', buyer=self.buyer, seller=self.seller, goods=self.goods1, price=100, address='x')
        Order.objects.create(order_no='A002', buyer=self.other, seller=self.seller, goods=self.goods2, price=200, address='x')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['order_no'], 'A001')

    def test_favorites_only_own_with_token(self):
        Favorite.objects.create(user=self.buyer, goods=self.goods1)
        Favorite.objects.create(user=self.other, goods=self.goods2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['goods_title'], '商品1')

    def test_cart_only_own_with_token(self):
        Cart.objects.create(user=self.buyer, goods=self.goods1)
        Cart.objects.create(user=self.other, goods=self.goods2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_messages_only_received_with_token(self):
        Message.objects.create(sender=self.seller, receiver=self.buyer, content='给 buyer')
        Message.objects.create(sender=self.seller, receiver=self.other, content='给 other')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], '给 buyer')

    def test_favorite_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/favorites/', {'goods': self.goods1.pk})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Favorite.objects.filter(user=self.buyer, goods=self.goods1).exists())

    def test_favorite_delete(self):
        favorite = Favorite.objects.create(user=self.buyer, goods=self.goods1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f'/api/favorites/{favorite.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Favorite.objects.filter(pk=favorite.pk).exists())

    def test_cart_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/cart/', {'goods': self.goods1.pk, 'quantity': 2})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Cart.objects.filter(user=self.buyer, goods=self.goods1).exists())
