from django.shortcuts import render, redirect, get_object_or_404
from gmail_authentication.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import pandas as pd
import os
from django.conf import settings
import pickle

def pred_form(request):
    # try:
    #     if request.session['name'] == 'SecretKey':
    emply = User.objects.all()
    return render(request, 'predictions/prediction.html', {'emply': emply})
    # except:
    #     return redirect('login')

def getUser(request):
    if request.method == "GET":
        user = request.GET.get('username', None)
        User_query = User.objects.get(username = user)
        # LikesGiven = int(Company.num_likes_given)
        # DislikesGiven = int(Company.num_dislikes_given)
        # LikesReceived = int(Company.num_likes_received)
        # DislikesReceived = int(Company.num_dislikes_received)
        # TotalVotes = int(Company.total_votes)
        # TotalVotes = int(Votes.objects.filter(id = User_query.id).count()) #benj
        # print(numVotes)
        departmentAlias = str(User_query.department)
        UserInstance = User.objects.get(username = user)
        UserID = UserInstance.id
        # TotalNoVotes = Votes.objects.filter(username = UserID).count()
        # AvgVotes = math.ceil(TotalVotes / TotalNoVotes)

        #dummy vals
        LikesGiven = int(6)
        DislikesGiven = int(0)
        LikesReceived = int(25)
        DislikesReceived = int(0)
        TotalVotes = int(8)
        AvgVotes = int (3)
        data = {'departmentAlias' : departmentAlias,
                'LikesGiven' : LikesGiven,
                'DislikesGiven' : DislikesGiven,
                'LikesReceived' : LikesReceived,
                'DislikesReceived' : DislikesReceived,
                'TotalVotes' : TotalVotes,
                'AvgVotes' : AvgVotes,
         }
        return JsonResponse(data)
# Create your views here.

@csrf_exempt
def predictpost(request):
    # try:
        if request.session['name'] == 'SecretKey':
            if request.method == "POST":
                departmentName = request.POST.get('departmentAlias')
                departmentInstance = Department.objects.get(department_name = departmentName)
                departmentAlias = int(departmentInstance.id)
                numVotes = request.POST.get('numVotes')
                votes = request.POST.get('vote')
                likes_given = request.POST.get('likes_given')
                dislikes_given =  request.POST.get('dislikes_given')
                likes = request.POST.get('likes')
                dislikes = request.POST.get('dislikes')
                #print(dislikes)
                columnName = ['departmentAlias', 'numVotes', 'votes', 'likes_given', 'dislikes_given', 'likes', 'dislikes']
                entry = [[departmentAlias, numVotes, votes, likes_given, dislikes_given, likes, dislikes]]
                path = os.path.join(settings.STATIC_DIR,'predictions/models/dt_model.benj')
                with open(path, 'rb') as file:
                    model = pickle.load(file)

                res = pd.DataFrame(entry)
                res.columns  = columnName
                result = model.predict(res)
                #print(result)
                user = request.POST.get('user')
                #print(user)
                UserInstance = User.objects.filter(username = user).update(prediction = result)
                #print(bool(result[0]))
                data = {
                  'username' : user,
                  'prediction' : bool(result[0]),
                }
                return JsonResponse(data)
            else:
                return HttpResponse("error")
    # except:
        return redirect('login')
