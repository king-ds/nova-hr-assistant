from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
# Create your views here.

def login(request):
    try:
        if request.session['name'] == 'SecretKey':
            return redirect('index')
    except:
            return render(request, 'admin_authentication/registration/login.html', {})

def authens(request):
    if request.method == "POST":
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['name'] = 'SecretKey'
            request.session['username'] = str(user.username)
            return redirect('admin_home')
        else:
            return redirect('login')

def logout(request):
    del request.session['name']
    del request.session['username']
    return redirect('login')