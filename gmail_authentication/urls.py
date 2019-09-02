from django.conf import settings
from . import views
from django.urls import path

urlpatterns = [
    path('welcome', views.welcome_page, name='welcome_page'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('configure-account/', views.configure_account, name='configure_account'),
    path('', views.home, name='home'),
]