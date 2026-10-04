from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('goods', views.GoodsViewSet, basename='goods')
router.register('orders', views.OrderViewSet, basename='order')
router.register('favorites', views.FavoriteViewSet, basename='favorite')
router.register('cart', views.CartViewSet, basename='cart')
router.register('messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', auth_views.obtain_auth_token, name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
