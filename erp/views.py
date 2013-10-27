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
from  forum.models import Forum, Topic, Post

# From python
import datetime

# From forms
from erp.forms import DepartmentForm, AddUserForm, SubDepartmentForm

# Consts
noperm = "You don't have permission to "

@login_required
def home(request):
    '''
        Renders the home page, display the name and a welcome message, have to change to preferred view
        based on user type
    '''
    return render_to_response('home.html',context_instance=RequestContext(request))
    
def login_user(request):
    '''
        Login handler
        Have to change all the HttpResponse to Alerts
    '''
    if request.user.is_authenticated():
        return render(request, 'alert.html', {'msg': 'You are already logged in', 'type': 'info'})
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user) # log in the user
                    return redirect('erp.views.home')
                else:
                    return render(request, 'login.html', {'msg': 'Account not active, contact admin. You have been suspended', 'type': 'warning'})
            else:
                print 'invalid'
                return render(request, 'login.html', {'msg': 'Incorrect Username or Password!', 'type': 'error'})
        else:
            next=request.path
            return render(request, 'login.html', {'next': next})

def logout_user(request):
    '''
        Logs out a user
    '''
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def page(request):
    '''
        Gen test view
    '''
    users_in_coords = Group.objects.get(name="Coords").user_set.all()
    users_in_cores = Group.objects.get(name="Cores").user_set.all()
    users_in_convenors = Group.objects.get(name="Convenors").user_set.all()

    if request.user in users_in_coords:
        state='Coord'
    elif request.user in users_in_cores:
        state='Core'
    elif request.user in users_in_convenors:
        state='Convenor'
    else:
        state='Unknown'
    html='Hello %s , Welcome to saarang erp, you are a %s ' % (request.user.username, state)
    return HttpResponse(html)

@login_required
def add_user(request):
    if not request.user.has_perm('erp.add_user'):
        return render(request, 'alert.html', {'msg': noperm + 'add user', 'type': 'error'})
    if request.method == 'POST':
        newuserForm = AddUserForm(request.POST)
        if newuserForm.is_valid():
            print "data valid"
            user = User.objects.create_user(username=newuserForm.cleaned_data['username'],
                                password=newuserForm.cleaned_data['password'])
            user.is_active = True
            # TODO : Add dept status and event, put alerts
            user.save()
        else:
            print "didnt validate"
    else:
        newuserForm = AddUserForm()
    to_return={
            'form':newuserForm,
            'action':  "",
            'title': "Add a new User"
        }
    return render(request, 'task/task.html', to_return)

@login_required
def add_dept(request):
    if not request.user.has_perm('erp.add_department'):
        return render(request, 'alert.html', {'msg': noperm + 'add departmnet', 'type': 'error'})
    if request.method == 'POST':
        deptForm = DepartmentForm(request.POST)
        if deptForm.is_valid():
            print "data valid"      
            deptForm.save()
        else:
            print "didnt validate"
    else:
        deptForm = DepartmentForm()
    to_return={
            'form':deptForm,
            'action':  "",
            'title': "Add a new Department"
        }
    return render(request, 'task/task.html', to_return)

@login_required
def add_subdept(request):
    if not request.user.has_perm('erp.add_subdepartment'):
        return render(request, 'alert.html', {'msg': noperm + 'add departmnet', 'type': 'error'})
    if request.method == 'POST':
        subdeptForm = SubDepartmentForm(request.POST)
        if subdeptForm.is_valid():
            print "data valid"      
            subdeptForm.save()
        else:
            print "didnt validate"
    else:
        subdeptForm = SubDepartmentForm()
    to_return={
            'form':subdeptForm,
            'action':  "",
            'title': "Add a new Sub Department"
        }
    return render(request, 'task/task.html', to_return)

@login_required
def contacts(request):
    contacts = []
    contacts = User.objects.all()
    to_return={
            'contacts': contacts,
        }
    return render(request, 'contacts.html', to_return)