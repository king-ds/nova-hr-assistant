from django.conf import settings
from . import views
from django.urls import path

urlpatterns = [
    path('home/', views.get_dept_vote, name='admin_home'),
    path('json/get_average_votes', views.get_avg_votes, name='get_average_votes'),
    path('json/get_total_data', views.get_total_data, name="get_total_data"),
    path('json/get_total_employee', views.get_total_employee, name="get_total_employee"),
    path('staff', views.staff, name="staff"),
    path('department', views.dept, name="department")
]
