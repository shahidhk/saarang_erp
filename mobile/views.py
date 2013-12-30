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
        return HttpResponse('n') # Not Registered
    if user.password == data['password']:
        if user.activate_status != 0:
            try:
                Device.objects.create(key=data['key'], user=user, last_access=dt.datetime.now(), is_active=True)
                user.last_login = dt.datetime.now()
                user.save()
            except:
                return HttpResponse('e') # General Error
            return HttpResponse('s') # Success
        else:
            return HttpResponse('a')# Account not activated 
    else:
        return HttpResponse('w') # Wrong password

@csrf_exempt
def register(request):
    ''' name mobile email password gender college '''
    data = request.POST.copy()
    if re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
        try:
            user=SaarangUser.objects.get(email=data['email'])
            return HttpResponse('r')# Already registered
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
                    return HttpResponse(str(new_user.saarang_id)) # Success response
                else:
                    return HttpResponse('w') # Passwords does not match
            else:
                return HttpResponse('p') # Mobile not 10 digits
    else:
        return HttpResponse('i') # Invalid email

@csrf_exempt
def logout(request):
    data=request.POST.copy()
    try:
        users = Device.objects.filter(key=data['key'], is_active=True)
        for user in users:
            user.is_active = False
            return HttpResponse('Success')
    except:
        return HttpResponse('Error')
