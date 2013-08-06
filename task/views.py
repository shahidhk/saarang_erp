# From Django
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.conf import settings
# From models
from task.models import Task, Comment

# From Forms
from task.forms import *

# From Python
import datetime as dt

def origin_task_create(request):
    if request.method == 'POST':
        otcForm = AddTaskForm(request.POST, request.FILES)
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
    hidden = (('Destination department', task.destin_dept), ('Created by', task.author), 
            ('Title', task.title), ('Summary', task.summary), ('Description', task.description), 
            ('Attachment', task.attachment), ('Deadline proposed', task.origin_deadline), 
            ('Priority assigned', task.origin_priority),)
    if request.method == 'POST':
        ocaForm = OriginCoreApprovalForm(data = request.POST, instance = task)
        if ocaForm.is_valid:
            data = ocaForm.save(commit=False)
            data.time_origin_core_approval = dt.datetime.now()
            data.save()
            ocaForm.save_m2m()
            # TODO : ckeckout the time is getting saved correctly
            task = get_object_or_404(Task, pk=task_id)
            ocaForm = OriginCoreApprovalForm(instance = task)
        else:
            print "didnt validate"
    else:
        ocaForm = OriginCoreApprovalForm(instance = task)
    to_return={
            'form':ocaForm,
            'action':  "",
            'title': "Approve task",
            'hidden': hidden
        }
        # TODO: destin_dept is shown as id, change it to Verbal
    return render(request, 'task/task.html', to_return)

def destin_core_approval(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    dcaForm = DestinCoreApprovalForm(instance = task)
    hidden = (('Destination department', task.destin_dept), ('Created by', task.author), 
            ('Title', task.title), ('Summary', task.summary), ('Description', task.description), 
            ('Attachment', task.attachment), ('Deadline proposed', task.origin_deadline), 
            ('Priority assigned', task.origin_priority), 
            ('Origin core approval', task.origin_core_aproved), ('Origin core comment', task.origin_core_comment), 
            ('Origin core deadline', task.origin_core_deadline), ('Origin core assigned priority', task.origin_core_priority), 
            ('Origin core assigned Coord', task.origin_core_assgnd_coord),)
    if request.method == 'POST':
        dcaForm = DestinCoreApprovalForm(data = request.POST, instance = task)
        if dcaForm.is_valid:
            data = dcaForm.save(commit=False)
            data.time_destin_core_approval = dt.datetime.now()
            data.save()
            dcaForm.save_m2m()
            # TODO : ckeckout the time is getting saved correctly
            dcaForm = DestinCoreApprovalForm(instance = task)
        else:
            print "didnt validate"
    else:
        dcaForm = DestinCoreApprovalForm(instance = task)
    to_return={
            'form':dcaForm,
            'action':  "",
            'title': "Approve task",
            'hidden': hidden
        }
        # TODO: destin_dept is shown as id, change it to Verbal
    return render(request, 'task/task.html', to_return)

def show_task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    to_return = {
                'task': task,
                'title': task.title,
                }   
    return render(request, 'task/show_task_details.html', to_return)

def my_task(request):
    tasks = Task.objects.filter(destin_core_assgnd_coord__id = request.user.id)
    to_return = {
                'tasks': tasks,
                'title': 'Tasks',
                }
    return render(request, 'task/show_task.html', to_return)

def dept_task(request):
    tasks = Task.objects.filter(destin_dept__id = request.user.userprofile.dept.id)
    print request.user.userprofile.dept
    to_return = {
                'tasks': tasks,
                'title': 'Tasks',
                }
    return render(request, 'task/show_task.html', to_return)