from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # 登录
    path('register/', views.register, name='register'),  # 注册
    path('logout/', views.logout, name='logout'),  # 注销用户
    path('user_info/', views.user_info, name='user_info'),  # 用户信息
]
