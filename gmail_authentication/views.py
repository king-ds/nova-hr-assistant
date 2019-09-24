# Python
import datetime
import facebook
import requests
import pandas as pd

# Django
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Application
from profile_feed.models import *
from .models import *
from background_task import background
from workplace_data.models import Post
from pypiper.scraper import DataScrape
from background_task.models import Task

token = {"DQVJ2SVdqcklvRTJfV2pjR3NuS05DVFRhZAmVlczNxMVBqZA1NwdWx0c2NPdDFnVmR0aXpYZAm4ySHBFT1Ywcjcyb25Ia09MZAFJIMWNOSWVaV085SlQ2TEF3UmN3dWQwX1JyNWVCajJxVHdIc2tBNVVFSUk0aS1yWjJZAclNNVjNpTDIzdVJrd3BMNXhfeVJvbVRXb2hfUGJhakgxZAzR1WHN0OEk0TTFHWEJOZA1ZAPYnVvS1VsMnN3NEtnLXVTTTNINlR4LUtYeXZAB"}
graph = facebook.GraphAPI(token,version='3.1')

# Background tasks
@background(schedule=0)
def pull_reactions_received(email):
	scrape = DataScrape(email)
	reaction_received = scrape.get_reaction_received()
	user_instance = User.objects.get(email=email)

	for key in reaction_received:
		Reaction.objects.filter(username=user_instance.id, reaction_type=key).update(reaction_received=reaction_received[key])

	print("[INFO] These reactions will be recorded %s" %reaction_received)

@background(schedule=0)
def pull_reactions_given(email):
	scrape = DataScrape(email)
	user_id = scrape.get_id()
	reaction_given = scrape.get_reaction_given(user_id)
	user_instance = User.objects.get(email=email)

	for key in reaction_given:
		Reaction.objects.filter(username=user_instance.id, reaction_type=key).update(reaction_given=reaction_given[key])

	print("[INFO] These reactions will be recorded %s" %reaction_given)

def pull_profile_picture(email):
	scrape = DataScrape(email)
	profile_picture = scrape.get_profile_picture()
	add_profile_photo = User.objects.filter(email=email).update(profile_picture=profile_picture)

@background(schedule=0)
def update_post(email):
	current_date = datetime.date.today() + datetime.timedelta(days=1)
	post_date_latest = Post.objects.latest('updated_time')
	week_lag =  current_date - datetime.timedelta(days=7)
	allgroups = list(Post.objects.order_by().values_list('group_id', flat=True).distinct())
	
	if current_date > (post_date_latest.updated_time.date() + datetime.timedelta(days=1)):
		print ("[INFO] Current date : %s is larger than latest Post date %s" %(current_date, post_date_latest.updated_time.date()))	
		columns_needed = ['group_id', 'post_id', 'message', 'updated_time', 'reactions']
		df_post = pd.DataFrame(columns=columns_needed)
		counter_group = 0
		counter_post = 0
		counter_reaction = 0

		for i in allgroups:
		    pull_post = graph.request(i + '/feed?fields=reactions, updated_time, message&limit=100&since='+ str(post_date_latest.updated_time.date()) + '&until=' + str(current_date))
		    counter_group += 1
		    print('[INFO] Pulling the data from group', i)

		    while pull_post['data']:
		        for post in pull_post['data']:
		            reaction_dict = dict()
		            counter_post += 1
		            ids = post['id'].split('_')
		            print('[INFO] Post ID: %s' %ids[1])
		            try: 
		                for reaction in post['reactions']['data']:
		                    counter_reaction += 1
		                    reaction_dict[reaction['id']] = reaction['type']
		                    print('[INFO] %s has %s this post: %s' %(reaction['id'], reaction['type'], ids[1]))

		            except KeyError as e:
		                print('[INFO] %s have no reaction' %ids[1])

		            try:
		                temp_post = pd.Series([ids[0], ids[1], post['message'], post['updated_time'], reaction_dict], index=columns_needed)
		                df_post = df_post.append(temp_post, ignore_index=True)

		            except KeyError as e:
		                temp_post = pd.Series([ids[0], ids[1], 'No Message', post['updated_time'], reaction_dict], index=columns_needed)
		                df_post = df_post.append(temp_post, ignore_index=True)
		        if 'next' in pull_post['paging'].keys():
		            pull_post = requests.get(pull_post['paging']['next']).json()
		            print('[INFO] End of page...')
		        else:
		        	break  
		    print ('[INFO] For Sanity Check; Total Groups: %d, Total Posts: %d, Total Reactions: %d' %(counter_group, counter_post, counter_reaction))

		for index, row in df_post.iterrows():
			is_post_exist = Post.objects.filter(post_id = row['post_id']).exists()
			if is_post_exist:
				pass
			else:	
				print(is_post_exist)
				p = Post(group_id=row['group_id'], post_id=row['post_id'], message=row['message'], updated_time=row['updated_time'], reactions=row['reactions'])
				p.save()
		#below is update
		columns_needed = ['group_id', 'post_id', 'message', 'updated_time', 'reactions']
		df_update = pd.DataFrame(columns=columns_needed)
		counter_group = 0
		counter_post = 0
		counter_reaction = 0

		for i in allgroups:
		    pull_post = graph.request(i + '/feed?fields=reactions, updated_time, message&limit=100&since='+ str(week_lag) + '&until=' + str(current_date))
		    counter_group += 1
		    print('[INFO] Pulling the data from group', i)

		    while pull_post['data']:
		        for post in pull_post['data']:
		            reaction_dict = dict()
		            counter_post += 1
		            ids = post['id'].split('_')
		            print('[INFO] Post ID: %s' %ids[1])
		            try: 
		                for reaction in post['reactions']['data']:
		                    counter_reaction += 1
		                    reaction_dict[reaction['id']] = reaction['type']
		                    print('[INFO] %s has %s this post: %s' %(reaction['id'], reaction['type'], ids[1]))

		            except KeyError as e:
		                print('[INFO] %s have no reaction' %ids[1])

		            try:
		                temp_post = pd.Series([ids[0], ids[1], post['message'], post['updated_time'], reaction_dict], index=columns_needed)
		                df_update = df_update.append(temp_post, ignore_index=True)

		            except KeyError as e:
		                temp_post = pd.Series([ids[0], ids[1], 'No Message', post['updated_time'], reaction_dict], index=columns_needed)
		                df_update = df_update.append(temp_post, ignore_index=True)
		        if 'next' in pull_post['paging'].keys():
		            pull_post = requests.get(pull_post['paging']['next']).json()
		            print('[INFO] End of page...')
		        else:
		        	break  
		    print ('[INFO] For Sanity Check; Total Groups: %d, Total Posts: %d, Total Reactions: %d' %(counter_group, counter_post, counter_reaction))
		
		Last_week = Post.objects.filter(updated_time__range=[current_date - datetime.timedelta(days=7), current_date])
		indexcnt = 0
		for index, row in df_update.iterrows():
			for last_row in Last_week:	
				if (last_row.group_id == row['group_id'] and last_row.post_id == row['post_id']):
					print ("[INFO] Group ID: %s and Post ID: %s are already stored in Database" %(row['group_id'], row['post_id']))
					indexcnt += 1
					Post.objects.filter(post_id=row['post_id']).update(message= row['message'], reactions = row['reactions'])
		print ("[INFO] %d posts are matched in the Database" %indexcnt)
		is_given_exist = Task.objects.filter(task_name='gmail_authentication.views.pull_reactions_given', task_params='[["%s"], {}]' %email).exists()
		is_received_exist = Task.objects.filter(task_name='gmail_authentication.views.pull_reactions_received', task_params='[["%s"], {}]' %email).exists()
		if not is_given_exist:
			pull_reactions_given(email)

		if not is_received_exist:
			pull_reactions_received(email)

	else:
		print ("[INFO] Post and reactions already updated")
		


# welcome page
def welcome_page(request):
    return render(request, 'gmail_authentication/welcome_page.html')

@login_required(login_url='welcome_page')
def configure_account(request):

	# Check for the existency of the user
	is_user_exist = User.objects.filter(username=request.user).exists()

	# If user already exist, automatically redirect the user to home page
	if is_user_exist:
		return redirect('home')

	# If button is clicked
	if request.method == 'POST':
		"""
		Get the following details
		"""
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		department = request.POST['department']

		# Look for department instance
		department_instance = get_object_or_404(Department, pk=department)

		# Create a new user
		new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, department=department_instance)
		# Commit
		new_user.save()
		# Increment by one the number of employees
		department_instance.add_employee()

		# Make a reaction object for new user
		user_instance = User.objects.get(username=request.user)
		
		for i in range(0,6):
			if i == 0:
				new_like_object = Reaction(username=user_instance, reaction_type='LIKE')
				new_like_object.save()
			elif i == 1:
				new_love_object = Reaction(username=user_instance, reaction_type='LOVE')
				new_love_object.save()
			elif i == 2:
				new_haha_object = Reaction(username=user_instance, reaction_type='HAHA')
				new_haha_object.save()
			elif i == 3:
				new_wow_object = Reaction(username=user_instance, reaction_type='WOW')
				new_wow_object.save()
			elif i == 4:
				new_sad_object = Reaction(username=user_instance, reaction_type='SAD')
				new_sad_object.save()
			else:
				new_angry_object = Reaction(username=user_instance, reaction_type='ANGRY')
				new_angry_object.save()

		pull_reactions_received(user_instance.email)
		pull_reactions_given(user_instance.email)
		pull_profile_picture(user_instance.email)

		return redirect('vote_page')

	# Additional data to be render in html forms
	context = {
		'departments' : Department.objects.all()
	}

	return render(request, 'gmail_authentication/configure_account.html', context)

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')