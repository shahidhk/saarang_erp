from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.models import User
import json
from models import Badge

def home(request):
    users = User.objects.all()
    mapping ={}
    for user in users:
        try:
            mapping[user.userprofile.barcode]= user.first_name
        except:
            pass
    to_return={
        'mapping':json.dumps(mapping),
    }
    return render(request, 'security/home.html', to_return)

def online(request):
    users = Badge.objects.all()
    mapping ={}
    for user in users:
        try:
            mapping[user.barcode]= user.name
        except:
            print 'error at user'
    to_return={
        'mapping':json.dumps(mapping),
    }
    return render(request, 'security/online.html', to_return)