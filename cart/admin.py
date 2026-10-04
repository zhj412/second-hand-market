from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'goods', 'quantity', 'created_at')
    search_fields = ('user__username', 'goods__title')
    raw_id_fields = ('user', 'goods')
