from django.conf import settings
from . import views
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
path('', views.login, name='login'),
path('authens', views.authens, name='authens'),
path('logout', views.logout, name='logout'),
path('home/', views.index, name='index'),
]