# From django
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse

# From models
from  models import Event

# From python
import datetime

# From forms
from forms import EventForm

# Consts
noperm = "You don't have permission to "

@login_required
def add_event(request):
    eventForm = EventForm()
    #if not request.user.has_perm('erp.add_event'):
    #    return render(request, 'alert.html', {'msg': noperm + 'add event', 'type': 'error'})
    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():
            print "data valid"      
            eventForm.save()
        else:
            print "didnt validate"
    else:
        eventForm = EventForm()
    to_return={
            'form':eventForm,
            'action':  "",
            'title': "Add a new Event"
        }
    return render(request, 'events/add_event.html', to_return)

@login_required
def list_events(request):
    events = Event.objects.all()
    to_return={
            'events':events,
        }
    return render(request, 'events/list_events.html', to_return)

@login_required
def details_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    to_return={
            'event':event,
        }
    return render(request, 'events/details_event.html', to_return)