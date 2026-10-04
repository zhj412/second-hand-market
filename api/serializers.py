"""DRF 序列化器：定义各资源的序列化 / 反序列化与字段校验。"""
from django.contrib.auth.models import User
from rest_framework import serializers

from cart.models import Cart
from favorite.models import Favorite
from goods.models import Category, Goods
from message.models import Message
from order.models import Order
from users.models import UserProfile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'parent', 'sort', 'is_active']


class GoodsSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Goods
        fields = [
            'id', 'title', 'description', 'price', 'original_price',
            'status', 'view_count', 'cover_image', 'created_at',
            'seller', 'seller_name', 'category', 'category_name',
        ]
        read_only_fields = ['seller', 'view_count', 'created_at', 'status']


class OrderSerializer(serializers.ModelSerializer):
    goods_title = serializers.CharField(source='goods.title', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_no', 'buyer', 'seller', 'seller_name',
            'goods', 'goods_title', 'price', 'status', 'address', 'created_at',
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    goods_title = serializers.CharField(source='goods.title', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'goods', 'goods_title', 'created_at']
        read_only_fields = ['user']


class CartSerializer(serializers.ModelSerializer):
    goods_title = serializers.CharField(source='goods.title', read_only=True)
    goods_price = serializers.DecimalField(source='goods.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'goods', 'goods_title', 'goods_price', 'quantity', 'created_at']
        read_only_fields = ['user']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'receiver', 'content', 'is_read', 'created_at']


class RegisterSerializer(serializers.Serializer):
    """注册接口：校验两次密码一致、用户名唯一，并创建用户 + 用户档案。"""

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=11)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password2': '两次密码输入不一致'})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'username': '用户名已存在'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        UserProfile.objects.create(
            user=user,
            phone=validated_data.get('phone', ''),
            nickname=validated_data['username'],
        )
        return user
