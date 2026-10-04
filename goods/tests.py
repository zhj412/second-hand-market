"""商品模块测试。

覆盖：
- Category 模型：字符串表示、自关联父子分类、默认值
- Goods 模型：字符串表示、默认状态、浏览量、时间排序
- 商品列表视图：只显示在售、关键词搜索、分类/价格筛选、排序
- 商品发布视图：登录保护、发布成功、必填字段校验
- 商品详情视图：正常展示、404、浏览量自增
"""
import tempfile
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from goods.models import Category, Goods

# 将测试期间上传的文件隔离到临时目录，避免污染真实的 media/ 目录
TEST_MEDIA_ROOT = tempfile.mkdtemp()


def make_image(name='cover.jpg'):
    """构造一个简单的测试图片文件对象。"""
    return SimpleUploadedFile(name, b'fake-image-content', content_type='image/jpeg')


class CategoryModelTest(TestCase):
    """Category 模型单元测试。"""

    def test_str_returns_name(self):
        category = Category.objects.create(name='数码产品')
        self.assertEqual(str(category), '数码产品')

    def test_default_sort_is_zero(self):
        category = Category.objects.create(name='数码产品')
        self.assertEqual(category.sort, 0)

    def test_is_active_defaults_true(self):
        category = Category.objects.create(name='数码产品')
        self.assertTrue(category.is_active)

    def test_parent_child_self_relation(self):
        parent = Category.objects.create(name='电子产品')
        child = Category.objects.create(name='手机', parent=parent)
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.children.all())


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class GoodsModelTest(TestCase):
    """Goods 模型单元测试。"""

    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.category = Category.objects.create(name='数码产品')

    def _make_goods(self, **kwargs):
        defaults = {
            'seller': self.seller,
            'category': self.category,
            'title': '测试商品',
            'description': '测试描述',
            'price': 100,
        }
        defaults.update(kwargs)
        defaults.setdefault('cover_image', make_image())
        return Goods.objects.create(**defaults)

    def test_str_returns_title(self):
        goods = self._make_goods(title='iPhone 13')
        self.assertEqual(str(goods), 'iPhone 13')

    def test_default_status_is_on_sale(self):
        goods = self._make_goods()
        self.assertEqual(goods.status, 'on_sale')

    def test_default_view_count_is_zero(self):
        goods = self._make_goods()
        self.assertEqual(goods.view_count, 0)

    def test_ordering_by_created_at_desc(self):
        old = self._make_goods(title='旧商品')
        new = self._make_goods(title='新商品')
        # auto_now_add 会忽略传入值，用 queryset.update() 显式设置时间以保证排序可断言
        Goods.objects.filter(pk=old.pk).update(created_at=timezone.now() - timezone.timedelta(days=1))
        Goods.objects.filter(pk=new.pk).update(created_at=timezone.now())
        titles = list(Goods.objects.values_list('title', flat=True))
        self.assertEqual(titles, ['新商品', '旧商品'])


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class GoodsListViewTest(TestCase):
    """商品列表视图测试。"""

    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.category = Category.objects.create(name='数码产品')
        self.other_category = Category.objects.create(name='图书')

    def _make_goods(self, **kwargs):
        defaults = {
            'seller': self.seller,
            'category': self.category,
            'title': '商品',
            'description': '测试描述',
            'price': 100,
            'status': 'on_sale',
        }
        defaults.update(kwargs)
        defaults.setdefault('cover_image', make_image())
        return Goods.objects.create(**defaults)

    def test_list_page_returns_200(self):
        response = self.client.get(reverse('goods:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_only_shows_on_sale_goods(self):
        self._make_goods(title='在售商品', status='on_sale')
        self._make_goods(title='已售商品', status='sold')
        self._make_goods(title='下架商品', status='off_sold')
        response = self.client.get(reverse('goods:list'))
        titles = [goods.title for goods in response.context['goods']]
        self.assertIn('在售商品', titles)
        self.assertNotIn('已售商品', titles)
        self.assertNotIn('下架商品', titles)

    def test_search_by_keyword(self):
        self._make_goods(title='iPhone 13 Pro')
        self._make_goods(title='Nike 运动鞋')
        response = self.client.get(reverse('goods:list'), {'q': 'iPhone'})
        titles = [goods.title for goods in response.context['goods']]
        self.assertIn('iPhone 13 Pro', titles)
        self.assertNotIn('Nike 运动鞋', titles)

    def test_filter_by_category(self):
        self._make_goods(title='iPhone', category=self.category)
        self._make_goods(title='Python 书', category=self.other_category)
        response = self.client.get(reverse('goods:list'), {'category': self.category.id})
        titles = [goods.title for goods in response.context['goods']]
        self.assertIn('iPhone', titles)
        self.assertNotIn('Python 书', titles)

    def test_filter_by_price_range(self):
        self._make_goods(title='便宜货', price=50)
        self._make_goods(title='中等货', price=500)
        self._make_goods(title='贵价货', price=5000)
        response = self.client.get(reverse('goods:list'), {'min_price': 100, 'max_price': 1000})
        titles = [goods.title for goods in response.context['goods']]
        self.assertIn('中等货', titles)
        self.assertNotIn('便宜货', titles)
        self.assertNotIn('贵价货', titles)

    def test_sort_by_price_ascending(self):
        self._make_goods(title='贵的', price=900)
        self._make_goods(title='便宜的', price=100)
        response = self.client.get(reverse('goods:list'), {'sort': 'price'})
        prices = [goods.price for goods in response.context['goods']]
        self.assertEqual(prices, sorted(prices))


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class GoodsPublishViewTest(TestCase):
    """商品发布视图测试。"""

    def setUp(self):
        self.user = User.objects.create_user(username='seller', password='pass12345')
        self.category = Category.objects.create(name='数码产品')

    def test_publish_requires_login(self):
        response = self.client.get(reverse('goods:publish'))
        self.assertEqual(response.status_code, 302)

    def test_publish_page_returns_200_when_logged_in(self):
        self.client.login(username='seller', password='pass12345')
        response = self.client.get(reverse('goods:publish'))
        self.assertEqual(response.status_code, 200)

    def test_publish_success_creates_goods(self):
        self.client.login(username='seller', password='pass12345')
        response = self.client.post(reverse('goods:publish'), {
            'title': 'iPhone 13',
            'category': self.category.id,
            'price': '4599.00',
            'original_price': '6999.00',
            'description': '95成新',
            'cover_image': make_image(),
        })
        goods = Goods.objects.get(title='iPhone 13')
        self.assertRedirects(response, reverse('goods:detail', kwargs={'pk': goods.pk}))
        self.assertEqual(goods.seller, self.user)
        self.assertEqual(goods.price, Decimal('4599.00'))
        self.assertEqual(goods.original_price, Decimal('6999.00'))

    def test_publish_without_cover_image_fails(self):
        self.client.login(username='seller', password='pass12345')
        self.client.post(reverse('goods:publish'), {
            'title': '无图商品',
            'category': self.category.id,
            'price': '100',
            'description': '没有封面图',
        })
        self.assertFalse(Goods.objects.filter(title='无图商品').exists())

    def test_publish_without_title_fails(self):
        self.client.login(username='seller', password='pass12345')
        self.client.post(reverse('goods:publish'), {
            'category': self.category.id,
            'price': '100',
            'cover_image': make_image(),
        })
        self.assertEqual(Goods.objects.count(), 0)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class GoodsDetailViewTest(TestCase):
    """商品详情视图测试。"""

    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass12345')
        self.category = Category.objects.create(name='数码产品')
        self.goods = Goods.objects.create(
            seller=self.seller,
            category=self.category,
            title='iPhone 13',
            description='测试描述',
            price=4599,
            cover_image=make_image(),
        )

    def test_detail_returns_200(self):
        response = self.client.get(reverse('goods:detail', kwargs={'pk': self.goods.pk}))
        self.assertEqual(response.status_code, 200)

    def test_detail_nonexistent_returns_404(self):
        response = self.client.get(reverse('goods:detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)

    def test_view_count_increments_on_each_visit(self):
        self.client.get(reverse('goods:detail', kwargs={'pk': self.goods.pk}))
        self.goods.refresh_from_db()
        self.assertEqual(self.goods.view_count, 1)
        self.client.get(reverse('goods:detail', kwargs={'pk': self.goods.pk}))
        self.goods.refresh_from_db()
        self.assertEqual(self.goods.view_count, 2)
