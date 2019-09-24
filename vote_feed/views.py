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
from django.db.models import Q
from pypiper.scraper import DataScrape
from background_task import background
from background_task.models import Task

def convert_timedelta(duration):
    seconds = duration.total_seconds()
    minutes = math.floor(seconds // 60)
    return minutes

@login_required(login_url='welcome_page')
def home(request):
	utc = pytz.UTC
	try:
		admin_access = ['ricardo.calura', 'christopher.cometa@novare.com.hk']

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

			# Check if recently logged in user have admin access
			if str(request.user) in admin_access:
				admin = True
				Comment = Votes.objects.all().order_by("-id")
			else:
				admin = False
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
			'admin' : admin,
		}
	except ObjectDoesNotExist:
		return HttpResponse('Please logout the admin account first and reload the page.')

	return render(request, 'vote_feed/vote_feed.html', context)

@csrf_exempt
def search_user(request):

	user_details = list()
	user_pictures = list()
	admin_access = ['ricardo.calura']

	if str(request.user) in admin_access:
		user = request.POST.get('user', None)
		if ' ' in user:
			user = user.split(' ')
			comments = Votes.objects.filter(Q(username__last_name__icontains=user[1]) | Q(username__first_name__icontains=user[0]))
		else:
			comments = Votes.objects.filter(Q(username__last_name__icontains=user) | Q(username__first_name__icontains=user))

		for comment in comments:
			user_details.append(comment.username.first_name+' '+comment.username.last_name)
			user_pictures.append(comment.username.profile_picture)
	
	data = {
		'comments' : list(comments.values()),
		'user_details' : user_details,
		'user_pictures' : user_pictures,
	}

	return JsonResponse(data)