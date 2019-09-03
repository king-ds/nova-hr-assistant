# Django
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Application
from profile_feed.models import *
from .models import *

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

		return redirect('vote_page')

	# Additional data to be render in html forms
	context = {
		'departments' : Department.objects.all()
	}

	return render(request, 'gmail_authentication/configure_account.html', context)

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')