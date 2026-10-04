"""DRF 视图集：提供各业务资源的 REST 接口。"""
from django.db.models import Q
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from cart.models import Cart
from favorite.models import Favorite
from goods.models import Category, Goods
from message.models import Message
from order.models import Order

from .serializers import (
    CartSerializer,
    CategorySerializer,
    FavoriteSerializer,
    GoodsSerializer,
    MessageSerializer,
    OrderSerializer,
    RegisterSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """分类接口（只读，公开）。"""

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class GoodsViewSet(viewsets.ModelViewSet):
    """商品接口：列表/详情公开，创建需登录。"""

    serializer_class = GoodsSerializer

    def get_queryset(self):
        qs = Goods.objects.filter(status='on_sale').select_related('seller', 'category')
        q = self.request.query_params.get('q')
        category_id = self.request.query_params.get('category')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """订单接口（只读，仅买家可见自己的订单）。"""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).select_related('goods', 'seller')


class FavoriteViewSet(viewsets.ModelViewSet):
    """收藏接口（仅本人可见、可增删）。"""

    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('goods')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    """购物车接口（仅本人可见、可增删改）。"""

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).select_related('goods')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """消息接口（只读，仅收件人可见）。"""

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user).select_related('sender')


class RegisterView(generics.CreateAPIView):
    """注册接口：创建用户并返回认证 Token。"""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'id': user.id, 'username': user.username, 'token': token.key},
            status=status.HTTP_201_CREATED,
        )
