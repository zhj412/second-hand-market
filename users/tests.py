"""用户模块测试。

覆盖：
- UserProfile 模型：字符串表示、可选字段、一对一关联
- 注册视图：成功注册、自动登录、密码不一致、用户名重复
- 登录视图：成功、密码错误、用户不存在
- 退出视图：跳转首页、会话清除
- 个人中心：登录保护、资料展示、资料更新
"""
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from users.models import UserProfile

# 将测试期间上传的头像隔离到临时目录，避免污染真实的 media/ 目录
TEST_MEDIA_ROOT = tempfile.mkdtemp()


class UserProfileModelTest(TestCase):
    """UserProfile 模型单元测试。"""

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')

    def test_str_returns_username(self):
        profile = UserProfile.objects.create(user=self.user, nickname='Alice')
        self.assertEqual(str(profile), 'alice')

    def test_optional_fields_default_to_none(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertIsNone(profile.phone)
        self.assertIsNone(profile.nickname)
        self.assertIsNone(profile.address)

    def test_one_to_one_relation_with_user(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(self.user.profile, profile)


class UserRegisterViewTest(TestCase):
    """注册视图功能测试。"""

    def test_get_register_page(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_success_creates_user_and_profile(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'password': 'abc12345',
            'password2': 'abc12345',
            'phone': '13800138000',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

    def test_register_auto_login_after_success(self):
        self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'password': 'abc12345',
            'password2': 'abc12345',
        })
        self.assertIn('_auth_user_id', self.client.session)

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'password': 'abc12345',
            'password2': 'different',
        })
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_duplicate_username_rejected(self):
        User.objects.create_user(username='taken', password='abc12345')
        self.client.post(reverse('users:register'), {
            'username': 'taken',
            'password': 'abc12345',
            'password2': 'abc12345',
        })
        self.assertEqual(User.objects.filter(username='taken').count(), 1)


class UserLoginViewTest(TestCase):
    """登录视图功能测试。"""

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')

    def test_get_login_page(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success_redirects_home(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'alice',
            'password': 'pass12345',
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_wrong_password_fails(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'alice',
            'password': 'wrong-password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_nonexistent_user_fails(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'ghost',
            'password': 'whatever',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class UserLogoutViewTest(TestCase):
    """退出视图功能测试。"""

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')
        self.client.login(username='alice', password='pass12345')

    def test_logout_redirects_home(self):
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('home'))

    def test_logout_clears_session(self):
        self.client.get(reverse('users:logout'))
        self.assertNotIn('_auth_user_id', self.client.session)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class UserProfileViewTest(TestCase):
    """个人中心视图测试。"""

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')

    def test_profile_requires_login(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_get_shows_data(self):
        self.client.login(username='alice', password='pass12345')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update_persists_changes(self):
        self.client.login(username='alice', password='pass12345')
        response = self.client.post(reverse('users:profile'), {
            'email': 'alice@example.com',
            'nickname': 'Alice',
            'phone': '13900139000',
            'address': '北京市朝阳区',
        })
        self.assertRedirects(response, reverse('users:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'alice@example.com')
        self.assertEqual(self.user.profile.nickname, 'Alice')
        self.assertEqual(self.user.profile.phone, '13900139000')
        self.assertEqual(self.user.profile.address, '北京市朝阳区')

    def test_profile_update_with_avatar(self):
        self.client.login(username='alice', password='pass12345')
        avatar = SimpleUploadedFile('avatar.jpg', b'fake-image', content_type='image/jpeg')
        response = self.client.post(reverse('users:profile'), {
            'nickname': 'Alice',
            'avatar': avatar,
        })
        self.assertRedirects(response, reverse('users:profile'))
        profile = UserProfile.objects.get(user=self.user)
        self.assertTrue(profile.avatar.name.endswith('avatar.jpg'))
