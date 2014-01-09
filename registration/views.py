# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render
from forms import SaarangUserForm
from models import SaarangUser
from django.contrib.auth.decorators import login_required
from random import *
from django.contrib import messages
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
        data=request.POST.copy()
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
            userform = SaarangUserForm()
            messages.success(request, data['desk_id'] +' Successfully saved')
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
            userform = SaarangUserForm()
            messages.success(request, userform.desk_id +' Successfully saved')
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

@login_required
def id_search(request):
    data=request.GET.copy()
    user_list = []
    users_id = SaarangUser.objects.filter(saarang_id__contains=data['q'].upper())[:10]
    users_email = SaarangUser.objects.filter(email__contains=data['q'].lower())[:10]
    users_name = SaarangUser.objects.filter(name__contains=data['q'])[:10]
    users_mobile = SaarangUser.objects.filter(mobile__contains=data['q'])[:10]
    for user in users_id:
        user_list.append({"id":user.id,'sid':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile })
    for user in users_email:
        user_list.append({"id":user.id,'sid':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile })
    for user in users_name:
        user_list.append({"id":user.id,'sid':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile })
    for user in users_mobile:
        user_list.append({"id":user.id,'sid':user.saarang_id, 'email':user.email, 'name':user.name, 'mobile':user.mobile })
    user_dict = json.dumps(user_list)
    return HttpResponse(user_dict)