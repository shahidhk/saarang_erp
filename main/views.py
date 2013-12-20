# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.middleware.csrf import get_token
import base64
from django.contrib import messages
from django.core.mail import send_mail
from registration.models import SaarangUser
from main.forms import ProfileEditForm,CreateTeamForm,EventOptionsForm
from events.models import Event,EventRegistration,Team


def auto_id(team_id):
    base = 'SA2014'
    num = "{0:0>3}".format(team_id)
    sid = base + num
    return sid

EVENT_WITH_OPTIONS = [35,50,17,52,46,26,7,15]

def home(request):
    return HttpResponse('HOME')

def get_csrf(request):
    to_return={
    'csrf':get_token(request),
    }
    return render(request, 'main/csrf.html', to_return)


def new_profile(request):
    data = request.POST.copy()
    try:
        user = get_object_or_404(SaarangUser, email=data['email'])
        return redirect('main_profile_edit', emailId=base64.encode(data['email']))
    except:
        new_user = SaarangUser.objects.create(email=data['email'],
        password=data['password'], name=data['name'],
        mobile=data['mobile'], gender=data['gender'], 
        college=data['college'])
        new_user.save()
        return redirect('main_profile_edit', emailId=base64.encode(data['email']))

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
        if event.id in EVENT_WITH_OPTIONS:
            return HttpResponseRedirect(reverse('band_details',kwargs={'eventId':eventId,'emailId':emailId,'teamId':teamId}))
        messages.info(request,'Already registered for the event')
    else:
        if not event.registration_open :
            messages.info(request,'Registration is closed for the event.')
        else:
            EventRegistration.objects.create(participant=user,team=team,event=event,options='')
            subject = 'Saarang 2014 Registration'
            email_msg = '\tYou have registered to the event \'%s\' under the team \'%s\' at Saarng 2014\n\n\nRegards,\n\tWeb-operations department\n\tSaaraang 2014' %(event.name,team.name)
            from_user = 'webadmin@saarang.org'
            mail_list = [member.email for member in team.members.all()]
            mail_list.append(email)
            send_mail(subject, email_msg, from_user,mail_list, fail_silently=False)

            if event.id in EVENT_WITH_OPTIONS:
                email = base64.b64encode(emailId)
                return HttpResponseRedirect(reverse('band_details',kwargs={'eventId':eventId,'emailId':emailId,'teamId':teamId}))
            messages.success(request,'Team registered successfully')
    return render(request, 'main/register_response.html')

def list_teams(request,eventId,emailId):
    to_return={}
    event = get_object_or_404(Event,id=eventId)
    email = base64.b64decode(emailId)
    user = get_object_or_404(SaarangUser,email=email)
    team_list = []
    reg_list=[]
    try:
        team_list += list(user.team_member.all())
    except:
        pass
    try:
        team_list += list(user.team_leader.all())
    except:
        pass
    event_reg = EventRegistration.objects.filter(event=event)
    for team in team_list:
        if event_reg.filter(team=team):
            if event.id in EVENT_WITH_OPTIONS:
                reg_list+=[3]
            else:
                reg_list+=[2]
        else:
            reg_list+=[1]
    team_list = zip(team_list,reg_list)
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
                    eventreg.options = ''
                    eventreg.save()
                    messages.success(request,'Registered successfully.')
                    subject = 'Saarang 2014 Registration'
                    email_msg = '\tYou have registered to the event \'%s\' at Saarang 2014\n\n\nRegards,\n\tWeb-operations department\n\tSaaraang 2014' %(event.name)
                    from_user = 'webadmin@saarang.org'
                    mail_list = [emailId]
                    try:
                        send_mail(subject, email_msg, from_user,mail_list, fail_silently=False)
                    except:
                        pass
                elif user.activate_status == 1:
                    messages.warning(request,'Please complete your profile to register for the event.')
                else:
                    messages.warning(request,'Click on the activation mail sent to activate your profile.')

        return render(request, 'main/register_response.html')

def create_team(request,emailId,eventId):
    emailId = base64.b64decode(emailId)
    user = get_object_or_404(SaarangUser,email=emailId)
    emailId=base64.b64encode(emailId)
    mail_list=[]
    if request.method == 'POST':
        createteamForm = CreateTeamForm(request.POST)   
        if createteamForm.is_valid():
            team_name = createteamForm.cleaned_data['team_name']
            team_members = createteamForm.cleaned_data['members']
            team = Team()
            team.name=team_name
            team.leader = user
            team.team_sid = '' 
            team.save()
            team.team_sid=auto_id(team.id)
            team.save()
            for member_email in team_members.split(','):
                try:
                    member = SaarangUser.objects.get(email=member_email)
                    team.members.add(member)
                    #mail_list.append(member_email)
                    msg = '%s has been added to the team' %(member)
                    messages.success(request,msg)
                except:
                    pass            
            subject = 'Saarang 2014 Registration'
            email_msg = '\tYou have been added to the team %s by %s\n\n\nRegards,\n\tWeb-Operations Department\n\tSaarang 2014' %(team.name,user)
            from_user = 'webadmin@saarang.org'
            try:
                send_mail(subject, email_msg, from_user,mail_list, fail_silently=False)
                msg = 'Confirmation mail sent'
                messages.success(request,msg)
            except:
                msg = 'Sending confirmation mail failed'
                messages.error(request,msg)
            team.save()
        return HttpResponseRedirect(reverse('list_teams',kwargs={'eventId':eventId,'emailId':emailId}))#,kwargs={'eventId':eventId,'teamId':teamId,}))
    else:
        createteamForm =  CreateTeamForm()
        to_return={
            'form':createteamForm,
            'emailId':emailId,
            'eventId':eventId,
        }
        return render(request, 'main/create_team.html',to_return)

def band_details(request,eventId,emailId,teamId):
    event = Event.objects.get(id=eventId)
    team = Team.objects.get(id=teamId)
    event_reg = EventRegistration.objects.get(event=event,team=team)
    options = event_reg.options
    print options
    try:
        options=options.split('|||')
        print options
    except:
        pass
    if request.method == 'POST':
        eventoptionsForm = EventOptionsForm(request.POST)
        if eventoptionsForm.is_valid():
            submisssion1 = eventoptionsForm.cleaned_data['submission1']
            submisssion2 = eventoptionsForm.cleaned_data['submission2']
            submisssion3 = eventoptionsForm.cleaned_data['submission3']
            band_email = eventoptionsForm.cleaned_data['band_email']
            options = 'url1===' + submisssion1 + '|||url2===' + submisssion2 + '|||url3===' + submisssion3 + '|||band_email===' + band_email 
            event_reg.options = options
            print options
            event_reg.save()
            messages.success(request,'Details saved successfully')
            return render(request, 'main/register_response.html')
    else:
        initial={}
        try:
            initial['submission1']=options[0].split('===')[1]
            print options[0].split('===')[1]
        except:
            pass
        try:
            initial['submission2']=options[1].split('===')[1]
            print options[1].split('===')[1]
        except:
            pass
        try:
            initial['submission3']=options[2].split('===')[1]
            print options[2].split('===')[1]
        except:
            pass
        try:
            initial['band_email']=options[3].split('===')[1]
            print options[3].split('===')[1]
        except:
            pass
        print initial
        eventoptionsForm = EventOptionsForm(initial=initial)
        if event.id in [35,17]:
            messages.info(request,'Please provide YouTube or Dropbox links to your <b>audio</b> submissions here.')
        else:
            messages.info(request,'Please provide YouTube or Dropbox links to your submissions here.')
        to_return = {
            'form':eventoptionsForm,
            'eventId':eventId,
            'emailId':emailId,
        }
        return render(request, 'main/band_details.html',to_return)
