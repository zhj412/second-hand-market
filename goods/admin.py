from django.contrib import admin
from .models import Category, Goods

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'sort', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'status', 'view_count', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    raw_id_fields = ('seller',)
