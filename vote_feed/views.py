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

utc=pytz.UTC

def convert_timedelta(duration):
    seconds = duration.total_seconds()
    minutes = math.floor(seconds // 60)
    return minutes

@login_required(login_url='welcome_page')
def home(request):

	try:
		admin_access = ['admin', 'christopher.cometa@novare.com.hk']
		
		# If user is authenticated
		if request.user.is_authenticated:
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
			reaction_summary = scrape.reaction_summary()
			print(reaction_summary)

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