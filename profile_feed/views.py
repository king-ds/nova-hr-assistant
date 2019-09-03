from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gmail_authentication.models import User

@login_required(login_url='welcome_page')
def profile(request, username):
	# Identify user
	user = User.objects.get(username=request.user)
	# Get the top 5 most liked post
	# Top_Posts = Post.objects.all().order_by("-num_likes")[:5]
	# Get user instance
	User_Instance = User.objects.get(username=request.user)
	# Get user posts
	# User_Posts = Post.objects.all().filter(username=User_Instance)
	# Rendered context
	context = {
		'first_name' : user.first_name,
		'last_name' : user.last_name,
		'username' : user.username,
		'email' : user.email,
		'date_joined' : user.datetime_joined,
        # 'Top_Posts' : Top_Posts,
        # 'User_Posts' : User_Posts,

	}
	return render(request, 'profile_feed/profile.html', context)

@login_required(login_url='welcome_page')
def about(request):
    return render(request, 'profile_feed/about.html')

def developer(request):
    return render(request, 'profile_feed/about_developer.html')