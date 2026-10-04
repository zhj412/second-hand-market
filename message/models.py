
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收者')
    content = models.TextField('消息内容')
    is_read = models.BooleanField('是否已读', default=False)
    created_at = models.DateTimeField('发送时间', auto_now_add=True)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'
