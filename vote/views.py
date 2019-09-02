from django.shortcuts import render , redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from vote.models import *
from gmail_authentication.models import *


# Create your views here.


# Views to serve the vote vote_page

@login_required(login_url='welcome')
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
	#is_poster = User.objects.get(username=request.user).selected_comment

	# If not both, redirect the user to home page
	if not is_voter and not is_poster:
		return redirect('home')

	# If not voter but poster, redirect user to comment page
	if not is_voter and is_poster:
		return redirect('add_post')

	context = {
		'User' : User.objects.get(username = request.user)
	}

	return render(request, 'vote/vote.html', context)




# Redirects to (add_post) after voting
@login_required(login_url='welcome')
def submit_vote(request):

    if request.method == "GET":

        vote = request.GET.get('Status', None)
        print(vote)
        userinstance = User.objects.get(username = request.user)
        voteinstance = Votes.objects.create(username = userinstance,votes = vote)
        userinstance.add_total_votes(int(vote))
        #User.objects.filter(username=request.user).update(selected_comment=True)
        User.objects.filter(username=request.user).update(selected_vote=False)

    return vote

def create_post(request):
    return render(request, 'vote/add_post.html')
