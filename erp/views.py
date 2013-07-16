from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from  forum.models import Forum, Topic, Post
import datetime

@login_required(login_url='/login/')
def home(request):
	name=request.user.first_name + " " + request.user.last_name
	return render_to_response('home.html', {'user': name}, context_instance=RequestContext(request))
	
def login_user(request):
	if request.user.is_authenticated():
		return HttpResponse('You are already logged in')
	else:
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('erp.views.home')
				else:
					return HttpResponse('<center>Account not active, contact Admin</center>')
			else:
				print 'invalid'
				return HttpResponse('<center>Invalid Login</center>')
		else:
			next="home"
			return render_to_response('login.html', {'next': next}, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponse('<center>logged out</center>')

def page(request):
	users_in_coords = Group.objects.get(name="Coords").user_set.all()
	users_in_cores = Group.objects.get(name="Cores").user_set.all()
	users_in_convenors = Group.objects.get(name="Convenors").user_set.all()

	if request.user in users_in_coords:
		state='Coord'
	elif request.user in users_in_cores:
		state='Core'
	elif request.user in users_in_convenors:
		state='Convenor'
	else:
		state='Unknown'
	html='Hello %s , Welcome to saarang erp, you are a %s ' % (request.user.username, state)
	return HttpResponse(html)

