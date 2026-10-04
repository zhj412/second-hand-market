from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'buyer', 'seller', 'goods', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_no', 'buyer__username', 'seller__username')
    raw_id_fields = ('buyer', 'seller', 'goods')
