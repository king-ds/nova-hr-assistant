from django.conf import settings
from . import views
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
]