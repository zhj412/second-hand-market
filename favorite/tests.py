"""收藏模块测试。

覆盖：
- Favorite 模型：字符串表示、用户-商品唯一约束
- 收藏列表视图：登录保护、只展示当前用户收藏
"""
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase, override_settings
from django.urls import reverse

from favorite.models import Favorite
from goods.models import Goods

# 将测试期间上传的文件隔离到临时目录
TEST_MEDIA_ROOT = tempfile.mkdtemp()


def make_image(name='cover.jpg'):
    return SimpleUploadedFile(name, b'fake-image-content', content_type='image/jpeg')


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FavoriteModelTest(TestCase):
    """Favorite 模型单元测试。"""

    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.goods = Goods.objects.create(
            seller=self.seller, title='商品', description='描述', price=100, cover_image=make_image(),
        )

    def test_str_contains_user_and_goods(self):
        favorite = Favorite.objects.create(user=self.user, goods=self.goods)
        self.assertEqual(str(favorite), 'u1 - 商品')

    def test_unique_constraint_on_user_and_goods(self):
        Favorite.objects.create(user=self.user, goods=self.goods)
        with self.assertRaises(IntegrityError):
            Favorite.objects.create(user=self.user, goods=self.goods)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FavoriteListViewTest(TestCase):
    """收藏列表视图测试。"""

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

    def test_favorite_requires_login(self):
        response = self.client.get(reverse('favorite:list'))
        self.assertEqual(response.status_code, 302)

    def test_shows_only_current_users_favorites(self):
        Favorite.objects.create(user=self.user, goods=self.goods1)
        Favorite.objects.create(user=self.other, goods=self.goods2)
        self.client.login(username='u1', password='pass12345')
        response = self.client.get(reverse('favorite:list'))
        titles = [favorite.goods.title for favorite in response.context['favorites']]
        self.assertIn('商品1', titles)
        self.assertNotIn('商品2', titles)
