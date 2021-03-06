import datetime as dt
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
import re, base64
from models import Device
from registration.models import SaarangUser
from registration.views import auto_id
from main.views import auto_id as team_id
from events.models import Event, EventRegistration, Team
from utility import send_push
from post_office import mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as erp_login
from userprofile.models import UserProfile
from events.models import Event,EventRegistration
from registration.models import SaarangUser

def saarang_decrypt(key):
    print key
    l = len(key)
    f4=key[:4]
    la=key[4-l:]
    return la+f4
    
def push(request):
    return render(request, 'mobile/push.html', {})

def push_send(request):
    data=request.POST.copy()
    result = send_push(data['push_text'])
    return render(request, 'alert.html', {'msg': result})

@csrf_exempt
def login(request):
    ''' Receive email, password, key via POST '''
    data = request.POST.copy()
    try:
        user = SaarangUser.objects.get(email=data['email'])
    except:
        return HttpResponse('Not_registerd') # Not Registered
    if user.password == data['password']:
        if user.activate_status != 0:
            try:
                existing_devices = Device.objects.filter(key=saarang_decrypt(data['key']))
                for device in existing_devices:
                    device.is_active = False
                    device.save()
            except:
                pass
            try:
                Device.objects.create(key=saarang_decrypt(data['key']), user=user, last_access=dt.datetime.now(), is_active=True)
                user.last_login = dt.datetime.now()
                user.save()
            except:
                return HttpResponse('Error') # General Error
            return HttpResponse(str(user.saarang_id)) # Success
        else:
            return HttpResponse('Account_not_activated')# Account not activated 
    else:
        return HttpResponse('Wrong_password') # Wrong password

@csrf_exempt
def register(request):
    ''' name mobile email password gender college '''
    data = request.POST.copy()
    print 'App: ', data
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
        try:
            user=SaarangUser.objects.get(email=data['email'])
            return HttpResponse('Registered')# Already registered
        except:
            if re.match(r'^\d{10}$', data['mobile']):
                if data['password'] == data['repassword'] and data['password'] !='':
                    mail.send(
                        [data['email']], template='email/main/register_activate',
                        context={'encoded_email':base64.b64encode(data['email']),}
                    )   
                    new_user=SaarangUser.objects.create(email=data['email'], mobile=data['mobile'], password=data['password'])
                    new_user.saarang_id = auto_id(new_user.pk)
                    # if data['college'] != '0':
                    #     college = College.objects.get(pk=data['college'])
                    #     new_user.college = college.name + ', ' + college.city
                    new_user.save()
                    return HttpResponse('Success') # Success response
                else:
                    return HttpResponse('Wrong_password') # Passwords does not match
            else:
                return HttpResponse('Phone_error') # Mobile not 10 digits
    else:
        return HttpResponse('Invalid_email') # Invalid email

@csrf_exempt
def logout(request):
    data=request.POST.copy()
    try:
        users = Device.objects.filter(key=saarang_decrypt(data['key']), is_active=True)
        for user in users:
            user.is_active = False
            user.save()
        return HttpResponse('Success')
    except:
        return HttpResponse('Error')

@csrf_exempt
def register_event(request):
    data = request.POST.copy()
    event = get_object_or_404(Event,id=int(data['event_id']))
    device = Device.objects.get(key=saarang_decrypt(data['key']), is_active=True)
    user = device.user
    if event.is_team:
        return HttpResponse('Team')
    else:
        if(EventRegistration.objects.filter(participant=user,event=event)):
            return HttpResponse('Already_registered')
        else:
            if not event.registration_open:
                return HttpResponse('Closed_registrations')
            else:
                if user.activate_status == 2 or user.activate_status == 1:
                    eventreg = EventRegistration()
                    eventreg.participant = user
                    eventreg.event = event
                    eventreg.options = ''
                    eventreg.save()
                    mail.send(
                        [user.email], template='email/main/register_event',
                        context={'event_name':event.long_name, }
                        )
                    return HttpResponse('Successfully_registered')
                #elif user.activate_status == 1:
                #    messages.warning(request,'Please complete your profile to register for the event.')
                else:
                    return HttpResponse('Not_activated')

@csrf_exempt
def set_session(request):
    data = request.POST.copy()
    device = Device.objects.get(key=saarang_decrypt(data['key']), is_active=True)
    user = device.user
    request.session['saaranguser_email'] = user.email
    return HttpResponse('Session_set')

@csrf_exempt
def get_session(request):
    data = request.POST.copy()
    device = Device.objects.get(key=saarang_decrypt(data['key']), is_active=True)
    user = device.user
    email = request.session.get('saaranguser_email')
    if email:
        return HttpResponse(email)
    else:
        return HttpResponse('None')
    try:
        user1 = SaarangUser.objects.get(email=email)
        return HttpResponse('Success '+user.email+' '+user1.email)
    except:
        return HttpResponse('Failed')

@csrf_exempt
def register_team(request):
    data = request.POST.copy()
    device = Device.objects.get(key=saarang_decrypt(data['key']), is_active=True)
    user = device.user
    event = get_object_or_404(Event, id=data['event_id'])
    team = Team.objects.create(name=data['team_name'], leader=user)
    team.team_sid = team_id(team.pk)
    team.save()
    mail_list=[]
    for member_email in re.findall(r'^[a-zA-Z0-9][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['team_members']):
        try:
            member = SaarangUser.objects.get(email=member_email)
            team.members.add(member)
            mail_list.append(member_email)
            team.save()
        except:
            return HttpResponse('Error')       
        try:
            mail.send(
            mail_list, template='email/main/added_to_team',
                    context={'team_name':data['team_name'], 'user':user,}
            )
        except:
            pass
        team.save()
    EventRegistration.objects.create(participant=user,team=team,event=event,options='')
    mail_list = [member.email for member in team.members.all()]
    mail_list.append(user.email)
    mail.send(
        mail_list, template='email/main/register_team',
                context={'event_name':event.long_name, 'team_name':team.name,},
                )
    return HttpResponse('Success')

@csrf_exempt
def mobileregistration(request):
    data=request.POST.copy()
    actionType = int(data['actionType'])
    try:
        userid = data['userid']
        eventid = int(data['eventid'])
    except:
        userid = "01SAA08"    
    if actionType == 4:
        event_list = ''
        events = Event.objects.all()
        for event in events:
            if event.is_team:
                is_team = '1'
            else:
                is_team = '0'
            buf = ':' + str(event.id) + ':' + event.long_name + ':' + is_team 
            event_list+=buf
        return HttpResponse(event_list) #list of all the events
    if actionType == 1:
        event = get_object_or_404(Event,id=eventid)
        users = userid.split('/') 
        if(len(users)>1):#Team regn
            lead = users.pop(0)
            leader = SaarangUser.objects.get(desk_id=lead)
            team = Team.objects.create(name=leader.name+'_team', leader=leader)
            team.team_sid=team_id(team.pk)
            team.save()
            mail_list=[]
            for barcode in users:
                try:
                    member = SaarangUser.objects.get(desk_id=barcode)
                    team.members.add(member)
                    team.save()
                    try:
                        mail_list.append(member.email)
                    except:
                        pass
                except:
                    pass
            team.save()
            try:
                mail.send(mail_list, template='email/main/added_to_team',
                    context={'team_name':leader.name+'_team',}
            )
            except:
                pass
            EventRegistration.objects.create(participant=leader,team=team,event=event,options='')
            return HttpResponse('Success')
        elif(len(users)==1):
            saaranguser = get_object_or_404(SaarangUser,desk_id = userid)
            if(EventRegistration.objects.filter(participant=saaranguser,event=event)):
                return HttpResponse('Already_registered')
            else:
                eventreg = EventRegistration()
                eventreg.participant = saaranguser
                eventreg.event = event
                eventreg.options = ''
                eventreg.save()
                mail.send(
                        [saaranguser.email], template='email/main/register_event',
                        context={'event_name':event.long_name, }
                )
                return HttpResponse('Successfully_registered')
    elif actionType == 2:
        event = get_object_or_404(Event,id=eventid)
        regs = event.reg_event.all()
        reg_list = ''
        for reg in regs:
            buf = reg.saarang_id + ':'
            reg_list+=buf
        return HttpResponse(reg_list) #list of all the registrations
    elif actionType == 3:
        event = get_object_or_404(Event,id=eventid)
        saaranguser = get_object_or_404(SaarangUser,saarang_id = userid)
        event_reg = get_object_or_404(EventRegistration,event=event,participant=saaranguser)
        event_reg.delete()
        return HttpResponse('Removed successfully')