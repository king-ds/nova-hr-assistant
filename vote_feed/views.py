# Python
import datetime
import math
import pytz

# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

# Application
from gmail_authentication.models import *
from vote.models import *
from pypiper.scraper import DataScrape
from background_task import background
from background_task.models import Task

utc=pytz.UTC

def convert_timedelta(duration):
    seconds = duration.total_seconds()
    minutes = math.floor(seconds // 60)
    return minutes

@background(schedule=0)
def scrape_reaction_received(email):
	scrape = DataScrape(email)
	reaction_given = scrape.get_reaction_given()

@background(schedule=0)
def fuck(email):
    print("Here we go again!")
    scrape = DataScrape(email)
    reaction_summary = scrape.get_reaction_received()
    print(scrape.get_reaction_given())

@login_required(login_url='welcome_page')
def home(request):

	try:
		admin_access = ['admin', 'christopher.cometa@novare.com.hk']

		# If user is authenticated
		if request.user.is_authenticated:

			# Check for the existency of the user
			is_user_exist = User.objects.filter(username=request.user).exists()

			if not is_user_exist:
				return redirect('configure_account')
			else:
				pass

			# Is user voter and poster?
			is_voter = User.objects.get(username=request.user).selected_vote

			# If user is voter, redirect her to vote page
			if is_voter:
				return redirect('vote_page')
			else:
				pass

			# Get the current user session
			user_instance = User.objects.get(username=request.user)

			# Scrape the data from workplace
			scrape = DataScrape(user_instance.email)
			
			# Check if background task is already in Task table
			is_task_exist = Task.objects.filter(task_params='[["%s"], {}]' %user_instance.email).exists()
			if not is_task_exist:
				fuck(user_instance.email)

			# Check if recently logged in user have admin access
			if str(request.user) in admin_access:
				Comment = Votes.objects.all().order_by("-id")
			else:
				Comment = Votes.objects.filter(username=user_instance).order_by("-id")

			User_Instance = User.objects.get(username = request.user)

			# Date Manipulation
			Date_Posts = []
			for votes_comment in Comment:
				Date_Posts.append(convert_timedelta(utc.localize(datetime.datetime.now()) - votes_comment.datetime_voted))

		else:
			return redirect('welcome')

		context = {
			'Comments': Comment,
			'User': User_Instance,
			'Date_Posts': Date_Posts,
		}
	except ObjectDoesNotExist:
		return HttpResponse('Please logout the admin account first and reload the page.')

	return render(request, 'vote_feed/vote_feed.html', context)
