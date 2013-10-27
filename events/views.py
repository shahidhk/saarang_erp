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
from models import Event
from erp.models import Department, SubDepartment
# From python
import datetime

# From forms
from forms import CreateEventForm,EventForm,EventRegistrationForm,IntroductionForm,FormatForm,FAQForm, PrizesForm

# Consts
noperm = "You don't have permission to "

@login_required
def add_event(request):
    # #if not request.user.has_perm('erp.add_event'):
    # #    return render(request, 'alert.html', {'msg': noperm + 'add event', 'type': 'error'})
    to_return={}
    if request.method == 'POST':
        status = request.user.userprofile.status
        subdept = request.user.userprofile.sub_dept
        eventForm = CreateEventForm(request.POST)
        if eventForm.is_valid():
            if status == 'coord' and eventForm.cleaned_data['sub_dept'] != subdept:
                return render(request, 'alert.html', {'msg': 'You dont have permission to create this event', 'type': 'error'})
            eventForm.save()
            return HttpResponseRedirect(reverse('list_events'))
        else:
            print "didnt validate"
    else:
        eventForm = CreateEventForm()
        to_return={
            'form':eventForm,
            'action':  "",
            'title': "Add a new Event"
        }
    return render(request, 'events/add_event.html', to_return)

@login_required
def list_events(request):
    events = Event.objects.all()
    if request.user.userprofile.status == 'core':
        pass
    elif request.user.userprofile.status == 'coord':
        events = events.filter(sub_dept=request.user.userprofile.sub_dept)
    to_return={
            'events':events,
        }
    return render(request, 'events/list_events.html', to_return)

@login_required
def details_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user.userprofile.status == 'core':
        pass
    elif request.user.userprofile.status == 'coord':
        if request.user.userprofile.sub_dept != event.sub_dept:
            return render(request, 'alert.html', {'msg': 'You dont have permission to access this event', 'type': 'error'})
    eventForm = EventForm(instance=event)
    faqForm = FAQForm(instance=event)
    introForm = IntroductionForm(instance=event)
    registrationForm = EventRegistrationForm(instance=event)
    formatForm = FormatForm(instance=event)
    prizesForm = PrizesForm(instance=event)
    to_return={
        'event': event,
        'form':eventForm,
        'form_intro':introForm,
        'form_reg':registrationForm,
        'form_prizes':prizesForm,
        'form_faq':faqForm,
        'form_format':formatForm,
        'action':  "",
        'title': "Add a new Event"
    }
    return render(request, 'events/event_details.html', to_return)

def event_det(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():
            event.name = eventForm.cleaned_data['name']
            event.google_group = eventForm.cleaned_data['google_group']
            event.save()
        else:
            print "didnt validate"
        return HttpResponseRedirect(reverse('details_event',args=(event.id,)))

def event_faq(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        faqForm = FAQForm(request.POST)
        if faqForm.is_valid():
            FAQs = faqForm.cleaned_data['FAQs']
            event.FAQs = FAQs
            event.save()
        else:
            print "didnt validate"
        return HttpResponseRedirect(reverse('details_event',args=(event.id,)))

def event_about(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        introForm = IntroductionForm(request.POST)
        if introForm.is_valid():
            about = introForm.cleaned_data['about']
            event.about = about
            event.save()
        else:
            print "didnt validate"
        return HttpResponseRedirect(reverse('details_event',args=(event.id,)))

def event_reg(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        registrationForm = EventRegistrationForm(request.POST)
        if registrationForm.is_valid():
            category = registrationForm.cleaned_data['category']
            registration_info = registrationForm.cleaned_data['registration_info']
            event.category = category
            event.registration_info = registration_info
            event.save()
        else:
            print "didnt validate"
        return HttpResponseRedirect(reverse('details_event',args=(event.id,)))

def event_format(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        formatForm = FormatForm(request.POST)
        if formatForm.is_valid():
            format = formatForm.cleaned_data['event_format']
            event.event_format = format
            event.save()
        else:
            print "didnt validate"
        return HttpResponseRedirect(reverse('details_event',args=(event.id,)))

def event_prizes(request,event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        prizeForm = PrizesForm(request.POST)
        if prizeForm.is_valid():
            prizes = prizeForm.cleaned_data['prizes']
            event.prizes = prizes
            event.save()
        else:
            print "didnt validate"
        return HttpResponseRedirect(reverse('details_event',args=(event.id,)))
