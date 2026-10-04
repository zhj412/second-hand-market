from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'欢迎回来，{user.username}！')
            return redirect('home')
        messages.error(request, '用户名或密码错误')
    return render(request, 'users/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone', '')
        if password != password2:
            messages.error(request, '两次密码输入不一致')
        elif User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
        else:
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, phone=phone, nickname=username)
            login(request, user)
            messages.success(request, '注册成功！')
            return redirect('home')
    return render(request, 'users/register.html')

def user_logout(request):
    logout(request)
    messages.success(request, '您已成功退出登录')
    return redirect('home')

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        profile.nickname = request.POST.get('nickname', profile.nickname)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, '个人信息已更新')
        return redirect('users:profile')
    return render(request, 'users/profile.html', {'profile': profile})
