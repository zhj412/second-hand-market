from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('', views.goods_list, name='list'),
    path('publish/', views.goods_publish, name='publish'),
    path('<int:pk>/', views.goods_detail, name='detail'),
]
