# Python
import datetime

# Django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Application
from gmail_authentication.models import User
from background_task.models import Task
from profile_feed.models import Reaction
from pypiper.scraper import DataScrape
from gmail_authentication.views import pull_reactions_given, pull_reactions_received, update_post

@login_required(login_url='welcome_page')
def profile(request, username):
	# Get user instance
	user_instance = User.objects.get(username=request.user)
	scrape = DataScrape(user_instance.email)
	profile_picture = scrape.get_profile_picture()
	title = scrape.get_title()
	department = scrape.get_department()
	reaction_given = dict.fromkeys(['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY'], 0)
	reaction_received = dict.fromkeys(['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY'], 0)
	for key in reaction_given:
		reaction = Reaction.objects.get(username=user_instance.id, reaction_type=key)
		reaction_given[key] += reaction.reaction_given
		reaction_received[key] += reaction.reaction_received

	# Rendered context
	context = {
		'first_name' : user_instance.first_name,
		'last_name' : user_instance.last_name,
		'username' : user_instance.username,
		'email' : user_instance.email,
		'date_joined' : user_instance.datetime_joined,
		'profile_picture': profile_picture,
		'title' : title,
		'department' : department,
		'reaction_given' : reaction_given,
		'reaction_received' : reaction_received,
	}
	return render(request, 'profile_feed/profile.html', context)

@login_required(login_url='welcome_page')
def about(request):
    return render(request, 'profile_feed/about.html')

def developer(request):
    return render(request, 'profile_feed/about_developer.html')

def refresh_profile(request):
	user_instance = User.objects.get(username=request.user)
	is_given_exist = Task.objects.filter(task_name='gmail_authentication.views.pull_reactions_given', task_params='[["%s"], {}]' %user_instance.email).exists()
	is_received_exist = Task.objects.filter(task_name='gmail_authentication.views.pull_reactions_received', task_params='[["%s"], {}]' %user_instance.email).exists()
	is_post_update_exist = Task.objects.filter(task_name='gmail_authentication.views.update_post', task_params='[["%s"], {}]' %user_instance.email).exists()
	
	if not is_post_update_exist:
		update_post(user_instance.email)


	data = {
		'is_post_update_exist' : is_post_update_exist,
		# 'is_received_exist' : is_received_exist,
	}
	return JsonResponse(data)