from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_list(request):
    orders = Order.objects.filter(buyer=request.user).select_related('goods', 'seller').order_by('-created_at')
    return render(request, 'order/list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    return render(request, 'order/detail.html', {'order': order})
