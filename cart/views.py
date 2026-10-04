from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart

@login_required
def cart_list(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('goods', 'goods__seller')
    return render(request, 'cart/list.html', {'cart_items': cart_items})
