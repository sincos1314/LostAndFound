from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User

from accounts.forms import RegisterForm, EditProfileForm
from accounts.models import Profile
from django.contrib.auth import authenticate

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data.get('email') or ''
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                college=form.cleaned_data['college'],
                class_name=form.cleaned_data['class_name'],
                gender=form.cleaned_data['gender'],
                phone=form.cleaned_data.get('phone') or None
            )
            messages.success(request, '注册成功，请登录')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        if not all([method, identifier, password]):
            messages.error(request, '请完整填写登录信息')
            return redirect('accounts:login')
        user = authenticate(request, identifier=identifier, password=password, method=method)
        if user:
            auth_login(request, user)
            messages.success(request, '登录成功，欢迎回来！')
            return redirect('home')
        else:
            messages.error(request, '登录失败，请检查账号与密码')
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, '已退出登录')
        return redirect('home')
    return HttpResponseBadRequest('Invalid method')

@login_required
def profile(request):
    prof = request.user.profile
    my_items = request.user.item_set.all().order_by('-created_at')
    return render(request, 'accounts/profile.html', {'prof': prof, 'my_items': my_items})

@login_required
def edit_profile(request):
    user = request.user
    prof = user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, user=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data.get('email') or ''
            user.save()
            prof.gender = form.cleaned_data['gender']
            prof.phone = form.cleaned_data.get('phone') or None
            prof.save()
            messages.success(request, '个人信息已更新')
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(initial={
            'username': user.username,
            'gender': prof.gender,
            'email': user.email,
            'phone': prof.phone or ''
        }, user=user)
    return render(request, 'accounts/edit_profile.html', {'form': form, 'prof': prof})

def login_options(request):
    identifier = request.GET.get('identifier')
    email_exists = False
    phone_exists = False
    if not identifier:
        return JsonResponse({'email_exists': False, 'phone_exists': False})
    # 支持用用户名或学号来探测绑定情况
    user = None
    # try username
    try:
        user = User.objects.get(username=identifier)
    except User.DoesNotExist:
        # try student_id
        try:
            prof = Profile.objects.get(student_id=identifier)
            user = prof.user
        except Profile.DoesNotExist:
            user = None
    if user:
        email_exists = bool(user.email)
        phone_exists = bool(getattr(user, 'profile', None) and user.profile.phone)
    return JsonResponse({'email_exists': email_exists, 'phone_exists': phone_exists})