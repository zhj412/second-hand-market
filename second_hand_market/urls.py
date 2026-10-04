from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

admin.site.site_header = '二手交易平台管理后台'
admin.site.site_title = '二手交易平台管理系统'
admin.site.index_title = '欢迎使用二手交易平台'

def home(request):
    from goods.models import Goods, Category
    goods_list = Goods.objects.filter(status='on_sale').select_related('seller', 'category')[:8]
    categories = Category.objects.filter(parent=None, is_active=True)
    return render(request, 'home.html', {'goods_list': goods_list, 'categories': categories})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('user/', include('users.urls')),
    path('goods/', include('goods.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('favorite/', include('favorite.urls')),
    path('message/', include('message.urls')),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
