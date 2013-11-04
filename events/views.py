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
from forms import *

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
            event = eventForm.save()
            print event
            coords= request.POST.getlist('coords')
            for coord_id in coords:
                coord = User.objects.get(pk=coord_id)
                coord.userprofile.events.add(event)
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
        events = request.user.userprofile.events.all()
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
        coord_events = request.user.userprofile.events.all()
        if event in coord_events:
            pass
        else:
            return render(request, 'alert.html', {'msg': 'You dont have permission to access this event', 'type': 'error'})
    coords_for_event = []
    for user in User.objects.all():
        try:
            for eve in user.get_profile().events.all():
                if eve == event:
                    coords_for_event.append(user.pk)
        except Exception, e:
            print e.message
        
    print coords_for_event
    eventForm = EventForm(instance=event, initial={'coords':coords_for_event } )
    faqForm = FAQForm(instance=event)
    introForm = IntroductionForm(instance=event)
    registrationForm = EventRegistrationInfoForm(instance=event)
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
            print 'valid'
            event.long_name = eventForm.cleaned_data['long_name']
            event.google_group = eventForm.cleaned_data['google_group']
            event.oneliner = eventForm.cleaned_data['oneliner']
            event.email = eventForm.cleaned_data['email'] 
            event.save()
            coords= request.POST.getlist('coords')
            for coord_id in coords:
                coord = User.objects.get(pk=coord_id)
                coord.userprofile.events.add(event)
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
        registrationForm = EventRegistrationInfoForm(request.POST)
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

def register(request):
    registerForm = EventRegistrationForm()
    if request.method == 'POST':
        registerForm = EventRegistrationForm(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            print registerForm.cleaned_data['event']
            event = Event.objects.get(long_name=registerForm.cleaned_data['event'])
            return HttpResponseRedirect(reverse('event_registrations', args=(event.id,)))
        else:
            print "didnt validate"
            registerForm = EventRegistrationForm(request.POST)
    to_return={
        'form': registerForm,
    }
    return render(request, 'events/register.html', to_return)

def list_registrations(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registrations = EventRegistration.objects.filter(event=event)
    to_return = {
        'event': event,
        'registrations': registrations,
    }
    return render(request, 'events/list_registrations.html', to_return)

def change_score(request, regn_id):
    regn = get_object_or_404(EventRegistration, pk=regn_id)
    changescoreForm = ChangeScoreForm(instance=regn)
    if request.method == 'POST':
        changescoreForm = ChangeScoreForm(request.POST)
        if changescoreForm.is_valid():
            regn.score = request.POST['score']
            regn.save()
            return HttpResponseRedirect(reverse('event_registrations', args=(regn.event.id,)))
        else:
            print "didnt validate"
            changescoreForm = ChangeScoreForm(request.POST)
    to_return={
        'form': changescoreForm,
    }
    return render(request, 'events/change_score.html', to_return)

def add_team(request):
    addteamForm = AddTeamForm()
    if request.method == 'POST':
        addteamForm = AddTeamForm(request.POST)
        if addteamForm.is_valid():
            addteamForm.save()
            return HttpResponseRedirect(reverse('register_event'))
        else:
            print "didnt validate"
            addteamForm = AddTeamForm(request.POST)
    to_return={
        'form': addteamForm,
    }
    return render(request, 'events/add_team.html', to_return)

def list_teams(request):
    teams = Team.objects.all()
    to_return={
        'teams': teams,
    }
    return render(request, 'events/list_teams.html', to_return)