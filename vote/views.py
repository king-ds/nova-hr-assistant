from django.shortcuts import render , redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from vote.models import *
from gmail_authentication.models import *


# Create your views here.


# Views to serve the vote vote_page

@login_required(login_url='welcome')
@csrf_exempt
def vote_page(request):

	# Check if user had logged in
	if request.user.is_authenticated:
		# Check if user is already exist in User Models
		is_user_exist = User.objects.filter(username=request.user).exists()
		# If not exist
		if not is_user_exist:
			# Redirect the user to configure account page
			return redirect('configure_account')
		# If exist
		else:
			pass

	# Verify the user if he/she allowed to vote and comment
	is_voter = User.objects.get(username=request.user).selected_vote


	# If not both, redirect the user to home page
	if not is_voter:
		return redirect('home')

	# If not voter but poster, redirect user to comment page
	if not is_voter:
		return redirect('vote_page')

	context = {
		'User' : User.objects.get(username = request.user)
	}

	return render(request, 'vote/vote.html', context)




# Redirects to (add_post) after voting
@csrf_exempt
def submit_vote(request):

	if request.method == "POST":

		vote = request.POST.get('vote', None)
		post = request.POST.get('post', None)
		userinstance = User.objects.get(username = request.user)
		voteinstance = Votes.objects.create(username = userinstance,votes = vote,comment=post)
		userinstance.add_total_votes(int(vote))
		User.objects.filter(username=request.user).update(selected_vote=False)

		data = {
			'status': 200
		}

	return JsonResponse(data)

# @login_required(login_url='welcome')
# @csrf_exempt
# def add_post(request):
#
# 	# Authenticate current user
# 	if request.user.is_authenticated:
# 		# If user made post request
# 		if request.method == "POST":
# 			"""
# 			Get the following details
# 			"""
# 			post = request.POST['post']
# 			print(post)
# 			user_instance = User.objects.get(username = request.user)
# 			add_post = Votes(username = user_instance, comment = post)
# 			# Add new post
# 			add_post.save()
# 			# Restrict user to avoid posting more
# 			# User.objects.filter(username=request.user).update(selected_comment=False)
# 			# Redirect user to home page
#
# 			return HttpResponseRedirect('Posted')
#
# 	# Extra context that will be render to add post page
# 	context = {
# 		'User' : User.objects.get(username = request.user)
# 	}
#
# 	return HttpResponseRedirect('Posted')
