from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'goods', 'created_at')
    search_fields = ('user__username', 'goods__title')
    raw_id_fields = ('user', 'goods')
