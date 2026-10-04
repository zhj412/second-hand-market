"""消息模块测试。

覆盖：
- Message 模型：字符串表示、已读状态默认值
- 消息列表视图：登录保护、只展示当前用户收到的消息
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from message.models import Message


class MessageModelTest(TestCase):
    """Message 模型单元测试。"""

    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass12345')
        self.receiver = User.objects.create_user(username='receiver', password='pass12345')

    def test_str_contains_sender_and_receiver(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='你好')
        self.assertEqual(str(message), 'sender -> receiver')

    def test_is_read_defaults_false(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='你好')
        self.assertFalse(message.is_read)


class MessageListViewTest(TestCase):
    """消息列表视图测试。"""

    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass12345')
        self.receiver = User.objects.create_user(username='receiver', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')

    def test_message_list_requires_login(self):
        response = self.client.get(reverse('message:list'))
        self.assertEqual(response.status_code, 302)

    def test_shows_only_received_messages(self):
        Message.objects.create(sender=self.sender, receiver=self.receiver, content='发给 receiver')
        Message.objects.create(sender=self.sender, receiver=self.other, content='发给 other')
        self.client.login(username='receiver', password='pass12345')
        response = self.client.get(reverse('message:list'))
        contents = [message.content for message in response.context['messages_received']]
        self.assertIn('发给 receiver', contents)
        self.assertNotIn('发给 other', contents)
