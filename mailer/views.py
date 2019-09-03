# Python
import math

# Django
from django.shortcuts import render
from django.http import JsonResponse
from gmail_authentication.models import User
from random import sample
from django.core.mail import send_mail

def random_mailer(request):
    total_user = User.objects.all()
    email_list = list()

    for user in total_user:
        email_list.append(user.email)
    
    randomize_users = sample(email_list, math.ceil(len(email_list)*0.50))

    for user in randomize_users:
        User.objects.filter(email=user).update(selected_vote=True)

    send_mail('Engage with your Co-workers','Join the fun! Visit now http://ec2-18-140-98-246.ap-southeast-1.compute.amazonaws.com:8000/','pypiper.developer@gmail.com', randomize_users, fail_silently=False)

    data = {
        'success':True,
        'count':len(randomize_users),
        }

    return JsonResponse(data)

def mailer_page(request):
    return render(request, 'mailer/mailer.html')