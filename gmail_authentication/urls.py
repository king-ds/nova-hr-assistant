from django.conf import settings
from . import views
from django.urls import path, include

urlpatterns = [
    path('welcome', views.welcome_page, name='welcome_page'),
    path('logout/', views.logout_user, name='logout'),
    path('configure-account/', views.configure_account, name='configure_account'),
    path('', views.home, name='home'),
]