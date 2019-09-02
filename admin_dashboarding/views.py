# Python
import math
import requests
import calendar
from datetime import datetime, timedelta
# Django
from django.shortcuts import render, redirect
from gmail_authentication.models import *
from vote.models import *
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg


def get_avg_votes(request):
    if request.method == "GET":
        company = request.GET.get('company')
        dataset = Votes.objects.values('username').annotate(vote_count=Avg('votes'))
        username = list()
        avg_votes = list()

        for entry in dataset:
            user_instance = User.objects.get(id=entry['username'])
            company_instance = Department.objects.get(department_name = company)
            is_company_employee = User.objects.filter(username = user_instance.username, department = company_instance.id).exists()

            if is_company_employee:
                votes_instance = user_instance.total_votes
                total_no_of_votes = Votes.objects.filter(username=user_instance.id).count()
                user_avg_votes = math.ceil(votes_instance/total_no_of_votes)
                avg_votes.append(user_avg_votes)
                username.append(user_instance.username)

        data  = {
            'username' : username,
            'avg_votes' : avg_votes,
        }
        return JsonResponse(data)

def get_total_data(request):
    if request.method == "GET":
        total_employees = User.objects.all().count()
        total_deparments = Department.objects.all().count()
        total_posts = Votes.objects.all().count()
        data = {'total_employees' : total_employees,
            'total_deparments' : total_deparments,
            'total_posts' : total_posts,
        }
    return JsonResponse(data)

def get_total_employee(request):
    if request.method == "GET":
        date_today = datetime.today()
        start_delta = timedelta(weeks=1)

        time_series = list()
        str_time_series = list()
        weekly_votes = list()

        for i in reversed(range(0,7)):
            str_time_series.append((date_today - timedelta(i)).date().strftime("%B %d %Y"))
            time_series.append((date_today - timedelta(i)).date())

        for i in time_series:
            month = i.month
            month_name = calendar.month_name[month]
            day = i.day
            year = i.year
            daily_votes = Votes.objects.filter(datetime_voted__year=year,datetime_voted__month=month,datetime_voted__day=day).count()
            weekly_votes.append(daily_votes)

        data = {
            'time_series' : str_time_series,
            'weekly_votes' : weekly_votes
        }
        return JsonResponse(data)

def home(request):
    if request.session['name'] == 'SecretKey':
        Users = User.objects.all()
        Departments = Department.objects.all()
        return render(request, 'admin_dashboarding/dashboard.html', {'Users' : Users, 'Departments' : Departments})
    else:
        return redirect('login')