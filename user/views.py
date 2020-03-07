from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm
from django.contrib.auth.models import User
from django.http import JsonResponse

# 登录
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))  # 'from'前端传进来的地址,没参数就返回首页
            else:
                login_form.add_error(None, '用户名或密码错误')
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

# 注册
def register(request):
    # 如果是post请求
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        # 进行用户验证
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']  # 参数由forms传
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 也可以这样创建用户
            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password(password)  #password做了保护,不能直接user.password = password
            # user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))  # 'from'由前端详情页传进来的地址,没参数就返回首页
    # 不是post请求
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context=context)

# 注销用户
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))  # 'from'前端传进来的地址,没参数就返回首页

# 用户信息
def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)