
from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', verbose_name='用户')
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE, related_name='cart_items', verbose_name='商品')
    quantity = models.IntegerField('数量', default=1)
    created_at = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'goods']

    def __str__(self):
        return f'{self.user.username} - {self.goods.title}'
