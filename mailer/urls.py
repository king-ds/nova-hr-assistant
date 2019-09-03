from django.conf import settings
from . import views
from django.urls import path

urlpatterns = [
    path('evaluate/', views.mailer_page, name='mailer_page'),
    path('send_mail/', views.random_mailer, name='random_mailer'),
]