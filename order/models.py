
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待付款'),
        ('paid', '待发货'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    order_no = models.CharField('订单号', max_length=50, unique=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_orders', verbose_name='买家')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_orders', verbose_name='卖家')
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE, related_name='orders', verbose_name='商品')
    price = models.DecimalField('成交价格', max_digits=10, decimal_places=2)
    status = models.CharField('订单状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    address = models.TextField('收货地址')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    pay_time = models.DateTimeField('付款时间', null=True, blank=True)
    ship_time = models.DateTimeField('发货时间', null=True, blank=True)
    complete_time = models.DateTimeField('完成时间', null=True, blank=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no
