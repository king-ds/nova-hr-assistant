from django.conf import settings
from . import views
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
path('prediction/', views.pred_form, name='pred_form'),
path('json/predict/', views.predictpost, name='predictpost'),
path('json/getUser/', views.getUser, name='getUser'),
]