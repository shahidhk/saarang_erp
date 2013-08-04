# From Django
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group

# From models
from task.models import Task, Comment

# From Forms
from task.forms import *

def origin_task_create(request):
    if request.method == 'POST':
        otcForm = AddTaskForm(request.POST)
        if otcForm.is_valid:
            print "data valid"
            data = otcForm.save(commit=False)
            data.author = request.user
            data.origin_dept = request.user.userprofile.dept
            data.save()
            otcForm.save()
        else:
            print "didnt validate"
    else:
        otcForm = AddTaskForm()
    to_return={
			'form':otcForm,
            'action':  "",
            'title': "Add a new Task"
		}
    return render(request, 'task/task.html', to_return)
    
def index(request):
    return  HttpResponse("HELLO")

def show_task(request):
    tasks = Task.objects.all()
    to_return = {
                'tasks': tasks,
                'title': 'Tasks',
                }   
    return render(request, 'task/show_task.html', to_return)

def origin_core_approval(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    ocaForm = OriginCoreApprovalForm(instance = task)
    if request.method == 'POST':
        ocaForm = OriginCoreApprovalForm(data = request.POST, instance = task)
        if ocaForm.is_valid:
            print "data valid"
            print ocaForm.errors
            ocaForm.save()
            ocaForm = OriginCoreApprovalForm(instance = task)
        else:
            print "didnt validate"
    else:
        ocaForm = OriginCoreApprovalForm(instance = task)
    to_return={
            'form':ocaForm,
            'action':  "",
            'title': "Approve task"
        }
    return render(request, 'task/task.html', to_return)

def show_task_details(request, task_id):
    tasks = Task.objects.all()
    to_return = {
                'tasks': tasks,
                'title': 'Tasks',
                }   
    return render(request, 'task/show_task.html', to_return)