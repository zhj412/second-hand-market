from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Goods, Category

def goods_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    sort = request.GET.get('sort', '-created_at')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    goods = Goods.objects.filter(status='on_sale').select_related('seller', 'category')
    
    if query:
        goods = goods.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    if category_id:
        goods = goods.filter(category_id=category_id)
    
    if min_price:
        goods = goods.filter(price__gte=float(min_price))
    
    if max_price:
        goods = goods.filter(price__lte=float(max_price))
    
    goods = goods.order_by(sort)
    categories = Category.objects.filter(parent=None, is_active=True)
    
    return render(request, 'goods/list.html', {
        'goods': goods,
        'categories': categories,
        'query': query,
        'current_category': int(category_id) if category_id else None,
    })

@login_required
def goods_publish(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        original_price = request.POST.get('original_price')
        description = request.POST.get('description')
        cover_image = request.FILES.get('cover_image')
        
        if title and price and cover_image:
            goods = Goods.objects.create(
                seller=request.user,
                category_id=category_id,
                title=title,
                price=price,
                original_price=original_price or None,
                description=description,
                cover_image=cover_image,
            )
            messages.success(request, '商品发布成功！')
            return redirect('goods:detail', pk=goods.pk)
        messages.error(request, '请填写完整信息')
    
    categories = Category.objects.filter(parent=None, is_active=True)
    return render(request, 'goods/publish.html', {'categories': categories})

def goods_detail(request, pk):
    goods = get_object_or_404(Goods, pk=pk)
    goods.view_count += 1
    goods.save(update_fields=['view_count'])
    return render(request, 'goods/detail.html', {'goods': goods})
