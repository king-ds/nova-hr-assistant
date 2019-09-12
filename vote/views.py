# Django
from django.shortcuts import render , redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Application
from vote.models import *
from gmail_authentication.models import *

# Views to serve the vote vote_page
@login_required(login_url='welcome_page')
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

		if int(vote) == 0:
			status = 400
		
		else:
			userinstance = User.objects.get(username = request.user)
			voteinstance = Votes.objects.create(username = userinstance,votes = vote,comment=post)
			userinstance.add_total_votes(int(vote))
			User.objects.filter(username=request.user).update(selected_vote=False)
			status = 200

		data = {
			'status': status
		}

	return JsonResponse(data)