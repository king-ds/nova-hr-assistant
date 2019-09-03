from django.conf import settings
from . import views
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
path('predict/', views.pred_form, name='prediction'),
path('json/predict/', views.predictpost, name='predictpost'),
path('json/getUser/', views.getUser, name='getUser'),
]