from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import datetime
@login_required(login_url='/login/')
def home(request):
		html='Hello %s , Welcome to saarang erp ' % request.user.username
		print 'authenticated'
		return HttpResponse(html)
	
def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
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