from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import datetime

def home(request):
	html='Welcome to saarang erp'
	return HttpResponse(html)
