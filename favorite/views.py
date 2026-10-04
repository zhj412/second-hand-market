from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Favorite

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('goods', 'goods__seller')
    return render(request, 'favorite/list.html', {'favorites': favorites})
