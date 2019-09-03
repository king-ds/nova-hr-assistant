from django.shortcuts import render, redirect, get_object_or_404
from gmail_authentication.models import *
from vote.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import datetime
import math
import pytz

utc=pytz.UTC
# Create your views here.

def convert_timedelta(duration):
    seconds = duration.total_seconds()
    minutes = math.floor(seconds // 60)
    return minutes

@login_required(login_url='welcome_page')
def home(request):

	# If user is authenticated
	if request.user.is_authenticated:
		
		# Is user voter and poster?
		is_voter = User.objects.get(username=request.user).selected_vote
		# is_poster = User.objects.get(username=request.user).selected_comment

		# If user is voter, redirect her to vote page
		if is_voter:
			return redirect('vote_page')

		# # if not voter but poster, redirect her to add post page
		# if not is_voter and is_poster:
		# 	return redirect('add_post')

		else:
			pass
		# Get all user's post
		Votess = Votes.objects.all().order_by("-id")
		# Get the top 5 most liked post
		# Top_Posts = Post.objects.all().order_by("-num_likes")[:5]
		# Get the current user session
		User_Instance = User.objects.get(username = request.user)
		# Filter 'Likes' model to fetch the post that was liked by current user
		# Liked_Object = Likes.objects.all().filter(username = User_Instance)
		# Liked_Posts = []

		# Date Manipulation
		Date_Posts = []
		for votes_c in Votess:
			print(votes_c.comment)
			Date_Posts.append(convert_timedelta(utc.localize(datetime.datetime.now()) - votes_c.datetime_voted))

	else:
		return redirect('welcome')

	context = {
		'Votess': Votess,
		'User': User_Instance,
		# 'Liked_Posts':Liked_Posts,
		# 'Top_Posts' : Top_Posts,
		'Date_Posts':Date_Posts,
	}

	return render(request, 'vote_feed/vote_feed.html', context)