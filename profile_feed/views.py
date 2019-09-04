from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gmail_authentication.models import User
from pypiper.scraper import DataScrape

@login_required(login_url='welcome_page')
def profile(request, username):
	# Get user instance
	user_instance = User.objects.get(username=request.user)
	scrape = DataScrape(user_instance.email)
	profile_picture = scrape.get_profile_picture()
	title = scrape.get_title()
	department = scrape.get_department()

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
	}
	return render(request, 'profile_feed/profile.html', context)

@login_required(login_url='welcome_page')
def about(request):
    return render(request, 'profile_feed/about.html')

def developer(request):
    return render(request, 'profile_feed/about_developer.html')