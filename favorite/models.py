
from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE, related_name='favorited_by', verbose_name='商品')
    created_at = models.DateTimeField('收藏时间', auto_now_add=True)

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'goods']

    def __str__(self):
        return f'{self.user.username} - {self.goods.title}'
