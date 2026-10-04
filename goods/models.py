
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField('分类名称', max_length=50)
    icon = models.CharField('图标', max_length=50, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父分类')
    sort = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']

    def __str__(self):
        return self.name

class Goods(models.Model):
    STATUS_CHOICES = [
        ('on_sale', '在售'),
        ('sold', '已售出'),
        ('off_sold', '下架'),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goods', verbose_name='卖家')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='goods_list', verbose_name='分类')
    title = models.CharField('商品标题', max_length=200)
    description = models.TextField('商品描述')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    original_price = models.DecimalField('原价', max_digits=10, decimal_places=2, blank=True, null=True)
    cover_image = models.ImageField('封面图', upload_to='goods/covers/')
    images = models.TextField('商品图片', blank=True, null=True)  # JSON存储多张图片
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='on_sale')
    view_count = models.IntegerField('浏览量', default=0)
    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title
