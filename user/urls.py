from django.urls import path, include
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup_success/', views.signup_success, name='signup_success'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('mypage/', views.my_page, name='mypage'),
    path('me/', views.me, name='me'),
    path('delete/', views.delete_user, name='delete_user'),
]