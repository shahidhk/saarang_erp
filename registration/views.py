# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render
from forms import SaarangUserForm
from models import SaarangUser
from django.contrib.auth.decorators import login_required
from random import *
import string
from post_office import mail

def auto_id(user_id):
    base = 'SA14W'
    num = "{0:0>5d}".format(user_id)
    sid = base + num
    return sid

@login_required
def add_user(request):
    if request.method == 'POST':
        userform =SaarangUserForm(request.POST)
        if userform.is_valid():
            user = userform.save()
            user.saarang_id = auto_id(user.pk)
            characters = string.ascii_letters + string.punctuation  + string.digits
            password =  "".join(choice(characters) for x in range(randint(8, 16)))
            user.password = password
            user.activate_status = 2
            user.save()
            mail.send(
                [user.email], template='email/main/activate_confirm',
                context={'saarang_id':user.saarang_id, 'password':user.password}
            )
            return HttpResponseRedirect(reverse('saarang_users'))
        else:
            userform = SaarangUserForm(request.POST)
    else:
        userform = SaarangUserForm()
    to_return={
            'form':userform,
            'action':  "",
            'title': "Add a new User"
        }
    return render(request, 'user_registration/new.html', to_return)

@login_required
def list_users(request):
    users = SaarangUser.objects.all()
    to_return={
            'users':users,
            'action':  "",
            'title': "Registered users"
        }
    return render(request, 'user_registration/list.html', to_return)

@login_required
def show_user(request, user_id):
    user = SaarangUser.objects.get(pk=user_id)
    userform = SaarangUserForm(instance=user)
    if request.method == 'POST':
        userform =SaarangUserForm(request.POST)
        if userform.is_valid():
            userform.save()
            return HttpResponseRedirect(reverse('saarang_users'))
        else:
            userform = SaarangUserForm(request.POST)
    else:
        userform = SaarangUserForm(instance=user)
    to_return={
            'form':userform,
            'action':  "",
            'title': "Add a new User"
        }
    return render(request, 'user_registration/new.html', to_return)
