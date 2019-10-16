from django.conf import settings
from . import views
from django.urls import path, include

urlpatterns = [
    path('profile/<str:username>', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('developer', views.developer, name='developer'),
    path('json/refresh_profile', views.refresh_profile, name='refresh_profile'),
    path('links/', views.useful_links, name='useful_links'),
]