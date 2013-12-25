import datetime as dt
from django.http import HttpResponseRedirect, HttpResponse, Http404

from models import Device
from registration.models import SaarangUser

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    data = request.POST.copy()
    try:
        user = SaarangUser.objects.get(email=data['email'])
    except:
        return HttpResponse('not_registerd')
    if user.password == data['password']:
        if user.activate_status != 0:
            try:
                Device.objects.create(key=data['key'], user=user, last_access=dt.datetime.now())
                user.last_login = dt.datetime.now()
                user.save()
            except:
                return HttpResponse('error')
            return HttpResponse('success')
        else:
            return HttpResponse('activate_account')
    else:
        return HttpResponse('password_wrong')

@csrf_exempt
def register(request):
    data = request.POST.copy()
    return HttpResponse('register')