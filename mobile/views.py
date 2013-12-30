import datetime as dt
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
import re, base64
from models import Device
from registration.models import SaarangUser
from registration.views import auto_id
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
                Device.objects.create(key=data['key'], user=user, last_access=dt.datetime.now())
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