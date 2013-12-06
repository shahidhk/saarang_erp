# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
import base64
from django.contrib import messages

from registration.models import SaarangUser
from main.forms import ProfileEditForm,CreateTeamForm
from events.models import Event,EventRegistration,Team

def main_profile_edit(request,emailId):
    emailId = base64.b64decode(emailId)
    print emailId
    user =  SaarangUser.objects.get(email=emailId)
    if request.method == 'POST':
        profileeditForm = ProfileEditForm(request.POST)
        if profileeditForm.is_valid():
            user.name = profileeditForm.cleaned_data['name']
            user.email = profileeditForm.cleaned_data['email']
            user.mobile = profileeditForm.cleaned_data['mobile']
            user.gender = profileeditForm.cleaned_data['gender']
            user.college = profileeditForm.cleaned_data['college']
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Profile updated successfully')
    else:
        initial = {'name': user.name,'email': user.email ,'mobile': user.mobile ,'gender':user.get_gender_display(),'college': user.college ,}
        profileeditForm = ProfileEditForm(initial=initial)
    to_return={
        'form':profileeditForm
    }

    return render(request, 'main/main_profile_edit.html', to_return)

def register_team(request,eventId,emailId,teamId):
    event = get_object_or_404(Event,id=eventId)
    team = get_object_or_404(Team,id=teamId)
    email = base64.b64decode(emailId)
    user = get_object_or_404(SaarangUser,email=email)
    if EventRegistration.objects.filter(event=event,team=team):
        messages.info(request,'Already registered for the event')
    else:
        if not event.registration_open :
            messages.info(request,'Registration is closed for the event.')
        else:
            EventRegistration.objects.create(participant=user,team=team,event=event)
            messages.success(request,'Team registered successfully')
    return render(request, 'main/register_response.html')

def list_teams(request,eventId,emailId):
    to_return={}
    event = get_object_or_404(Event,id=eventId)
    email = base64.b64decode(emailId)
    user = get_object_or_404(SaarangUser,email=email)
    team_list = list(user.team_member.all())
    for team in list(user.team_leader.all()):
        team_list.append(team)
    to_return = {
        'team_list':team_list,
        'user':user,
        'eId':event.id,
        'emailId':emailId,
    }    
    return render(request, 'main/list_teams.html',to_return)

def register(request,eventId,emailId):
    event = get_object_or_404(Event,id=eventId)
    if event.is_team:
        return HttpResponseRedirect(reverse('list_teams',kwargs={'eventId':eventId,'emailId':emailId}))#,kwargs={'eventId':eventId,'teamId':teamId,}))
    else:
        emailId = base64.b64decode(emailId)
        user = get_object_or_404(SaarangUser,email=emailId)
        if(EventRegistration.objects.filter(participant=user,event=event)):
            messages.info(request,'Already registered for the event.')
        else:
            if not event.registration_open:
                messages.info(request,'Registration is closed for the event.')
            else:
                if user.activate_status == 2:
                    eventreg = EventRegistration()
                    eventreg.participant = user
                    eventreg.event = event
                    eventreg.save()
                    messages.success(request,'Registered successfully.')
                elif user.activate_status == 1:
                    messages.warning(request,'Please complete your profile to register for the event.')
                else:
                    messages.warning(request,'Click on the activation mail sent to activate your profile.')

        return render(request, 'main/register_response.html')

def create_team(request,emailId,eventId):
user = get_object_or_404(SaarangUser,email=emailId)
    if request.method == 'POST':
        createteamForm = CreateTeamForm(request.POST)   
        if createteamForm.is_valid():
            team_name = createteamForm.cleaned_data['team_name']
            team_members = createteamForm.cleaned_data['members']
            for members in team_members.split(','):
                 
    else:
        createteamForm =  CreateTeamForm()
        to_return={
            'form':createteamForm,
        }
    return render(request, 'main/create_team.html',to_return)
