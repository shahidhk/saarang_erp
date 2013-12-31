import datetime as dt
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
import re, base64
from models import Device
from registration.models import SaarangUser
from registration.views import auto_id
from events.models import Event, EventRegistration
from utility import send_push
from post_office import mail
from django.views.decorators.csrf import csrf_exempt

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
                existing_devices = Device.objects.filter(key=data['key'])
                for device in existing_devices:
                    device.is_active = False
                    device.save()
            except:
                pass
            try:
                Device.objects.create(key=data['key'], user=user, last_access=dt.datetime.now(), is_active=True)
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
    if re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
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
        users = Device.objects.filter(key=data['key'], is_active=True)
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
    device = Device.objects.get(key=data['key'], is_active=True)
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
