# Django
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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

		return redirect('vote_page')

	# Additional data to be render in html forms
	context = {
		'departments' : Department.objects.all()
	}

	return render(request, 'gmail_authentication/configure_account.html', context)

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='welcome_page')
def home(request):

	# If user is authenticated
	if request.user.is_authenticated:

		# Is user voter and poster?
		is_voter = User.objects.get(username=request.user).selected_vote
		#is_poster = User.objects.get(username=request.user).selected_comment

		# If user is voter, redirect her to vote page
		if is_voter:
			return redirect('vote_page')

		# if not voter but poster, redirect her to add post page
		if not is_voter and is_poster:
			return redirect('add_post')

		else:
			pass
		# Get all user's post
		Posts = Post.objects.all().order_by("-id")
		# Get the top 5 most liked post
		Top_Posts = Post.objects.all().order_by("-num_likes")[:5]
		# Get the current user session
		User_Instance = User.objects.get(username = request.user)
		# Filter 'Likes' model to fetch the post that was liked by current user
		Liked_Object = Likes.objects.all().filter(username = User_Instance)
		Liked_Posts = []

		# Date Manipulation
		Date_Posts = []
		for post in Posts:
			Date_Posts.append(convert_timedelta(datetime.datetime.now() - post.datetime_comments))
			for like in Liked_Object:
				if post.id == like.post.id:
					Liked_Posts.append(like.post.id)
	else:
		return redirect('welcome')

	context = {
		'Posts': Posts,
		'User': User_Instance,
		'Liked_Posts':Liked_Posts,
		'Top_Posts' : Top_Posts,
		'Date_Posts':Date_Posts,
	}

	return render(request, 'gmail_authentication/welcome_page.html', context)
