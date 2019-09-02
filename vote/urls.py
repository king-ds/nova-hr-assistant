from django.urls import path
from . import views

urlpatterns = [
    path('vote/new/', views.vote_page, name='vote_page'),
    path('vote/submit/', views.submit_vote, name='submit_vote'),

]
