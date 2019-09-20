# Python
import math
import requests
import calendar
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import altair as alt
import numpy as np
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
    chart = alt.Chart(pd.DataFrame(),title='No Users Yet').mark_bar()
    chart_2 = alt.Chart(pd.DataFrame(),title='No Users Yet').mark_bar()
    chart_3 = alt.Chart(pd.DataFrame(),title='No Users Yet').mark_bar()
    user = User.objects.all().values('id','department')
    department = Department.objects.all().values('id','department_name')
    votes = Votes.objects.all().values('username','department_name','votes')
    reactions = Reaction.objects.all().values('username','reaction_given','reaction_received','reaction_type')
    #check if the query set for user is empty
    if not user:
        # assign empty graphs if there are no users.
        chart = alt.Chart(pd.DataFrame(),title='No Users Yet').mark_bar()
        chart_2 = alt.Chart(pd.DataFrame(),title='No Users Yet').mark_bar()
        chart_3 = alt.Chart(pd.DataFrame(),title='No Users Yet').mark_bar()
    else:
        user = pd.DataFrame(user)
        user.columns = ['user_id','dept_id']
        department = pd.DataFrame(department)
        department.columns = ['dept_id','Department Name']
        user = pd.merge(user,department,on=['dept_id'])
        #check if the query set for votes is empty
        if not votes:
            chart = alt.Chart(pd.DataFrame(),title='No Users Yet').mark_bar()
        else:
            votes = pd.DataFrame(votes)
            votes.columns = ['user_id','dept_id','votes']
            user_dept_votes = pd.merge(user,votes,on=['user_id','dept_id'])
            dept_votes = pd.pivot_table(index=['Department Name'],values='votes',aggfunc=np.mean,data=user_dept_votes).reset_index()
            dept_votes.columns = ['Department Name','Votes']
            dept_votes['Votes'] = dept_votes['Votes'].apply(math.ceil)



            # Render Vote Chart If there are votes
            chart =  alt.Chart(dept_votes).mark_bar().encode(
            x=alt.X('Votes:Q',axis=alt.Axis(values=[1,2,3,4])),
            color= alt.Color('Votes:O', scale=alt.Scale(domain=[1,2,3,4],range=['red','red','orange','lightgreen'])),
            row='Department Name:N'
            ).properties(
                height = 50,
                width = 800
                )


            # check if there are empty reactions
            if not reactions:
                chart_3 = alt.Chart(pd.DataFrame(),title='No Users Yet').mark_bar()
            else:
                reactions = pd.DataFrame(reactions)
                reactions.columns = ['user_id','Reactions Given','Reactions Received','Reaction Type']
                reactions = pd.merge(user,reactions,on=['user_id'])


                brush = alt.selection_interval()
                chart_x = alt.Chart(reactions).mark_bar().encode(
                    y = 'Reaction Type:N',
                    x = 'sum(Reactions Given):Q',
                    color = alt.condition(brush,alt.value('lightgray'),'Department Name:N')
                    ).add_selection(brush)
                chart_y = chart_x.encode(x = 'sum(Reactions Received):Q')
                chart_3 = chart_x | chart_y








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
