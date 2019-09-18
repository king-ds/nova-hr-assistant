# Python
import math
import requests
import calendar
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import altair as alt
pd.set_option('display.max_columns', None)

# Django
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg

# Application
from gmail_authentication.models import *
from vote.models import *
from profile_feed.models import *

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


def get_dept_vote(request):
    dept_list = []
    vote_list = []
    dept_name_list = []
    act_vote_list = []
    departments = Department.objects.all().values('department_name')
    for department in departments:
        dept_list.append(department['department_name'])
    for i in dept_list:
        instance = Department.objects.get(department_name=i)
        vote_list.append(Votes.objects.filter(department_name=instance))
    for i in vote_list:
        for j in i:
            dept_name_list.append(str(j.department_name))
            act_vote_list.append(j.votes)

    user = User.objects.all().values('id','department')
    userer = pd.DataFrame(user)
    userer.columns=['user_id','dept_id']
    reaction = Reaction.objects.all().values('username','reaction_given','reaction_received','reaction_type')
    reacter = (pd.DataFrame(reaction))
    reacter.columns = ['user_id','reaction_given','reaction_received','reaction_type']
    depter = Department.objects.all().values('department_name','id')
    depteter = (pd.DataFrame(depter))
    depteter.columns = ['department_name','dept_id']
    voter = Votes.objects.all().values('username','votes','department_name')
    voter = (pd.DataFrame(voter))
    voter.columns = ['user_id','votes','dept_id']
    voter = pd.pivot_table(index='dept_id',values='votes',aggfunc=np.mean,data=voter)
    voter['votes'] = voter['votes'].apply(math.ceil)
    usdep = (pd.merge(userer,depteter,on='dept_id'))
    summary = (pd.merge(usdep,reacter,on='user_id'))
    test = pd.pivot_table(index='reaction_type',values=['reaction_given','reaction_received'],aggfunc=sum,data=summary).reset_index()
    summary = (pd.pivot_table(index=['user_id','dept_id','department_name'],values=['reaction_given','reaction_received'],aggfunc=sum,data=summary).reset_index())
    final = pd.merge(summary,voter,on=['dept_id'])
    #print(test)


    # brush = alt.selection(type='interval', encodings=['x'],empty='none')
    #
    # bars = alt.Chart().mark_bar().encode(
    # x='reaction_given:O',
    # y='count()',
    # color=alt.condition(brush, 'reaction_type:O', alt.value('lightgray'))
    # ).add_selection(
    # brush
    # )
    #
    # chart_3 = alt.layer(bars, data=test).properties(width = 500)

    brush = alt.selection(type='interval', encodings=['x'],empty='none')


    base = alt.Chart().mark_bar().encode(
    x=alt.X(alt.repeat('column'), type='quantitative', bin=alt.Bin(maxbins=20)),
    y='count()',
    tooltip='reaction_type'

    ).properties(
    width=350,
    height=350
    )

    background = base.add_selection(brush)

    highlight = base.encode(
    color='reaction_type'
    ).transform_filter(brush)

    # layer the two charts & repeat alt.value('goldenrod')
    chart_3 = alt.layer(
    background,
    highlight,
    data=test).repeat(column=["reaction_given","reaction_received"])









    frame = pd.DataFrame(dept_name_list)
    frame.columns = ['Department']
    frame['Votes'] = act_vote_list
    frame = pd.pivot_table(index='Department',values='Votes',aggfunc=np.mean,data=frame).reset_index()
    frame['Votes'] = frame['Votes'].apply(math.ceil)
    context = locals()
    source = frame

    chart =  alt.Chart(source).mark_bar().encode(
    x=alt.X('Votes:Q',axis=alt.Axis(values=[1,2,3,4])),
    color= alt.Color('Votes:O', scale=alt.Scale(domain=[1,2,3,4],range=['red','lightred','orange','lightgreen'])),
    row='Department:N'
    ).properties(
        height = 50,
        width = 800
        )





    if request.method == "GET":
        date_today = datetime.today()
        start_delta = timedelta(weeks=1)

        time_series = list()
        str_time_series = list()
        weekly_votes = list()

        for i in reversed(range(0,8)):
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

        data = pd.DataFrame(data)
        data.columns = ['Date','Number of Votes']
        data['Date'] = pd.to_datetime(data['Date'])


        chart_2 = alt.Chart(data).mark_line().encode(
            x = alt.X('Date:T'),
            y = 'Number of Votes:Q'
        ).properties(
            height=250,
            width=800
            )


        # context['chart'] = chart_1
        if request.method == "GET":
            total_employees = User.objects.all().count()
            total_deparments = Department.objects.all().count()
            total_posts = Votes.objects.all().count()
            datas = {'total_employees' : total_employees,
                'total_deparments' : total_deparments,
                'total_posts' : total_posts,
                'chart' : chart,
                'chart_2' : chart_2,
                'chart_3' : chart_3,
            }








    return render(request, 'admin_dashboarding/test.html', datas)





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
        Comments = Votes.objects.all()
        return render(request, 'admin_dashboarding/dashboard.html', {'Users' : Users, 'Departments' : Departments, 'Comments': Comments})
    else:
        return redirect('login')
