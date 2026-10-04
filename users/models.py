
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('手机号', max_length=11, blank=True, null=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    nickname = models.CharField('昵称', max_length=50, blank=True, null=True)
    address = models.TextField('收货地址', blank=True, null=True)
    created_at = models.DateTimeField('注册时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
