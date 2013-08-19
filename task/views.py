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

noperm = "You don't have permission to "

def origin_task_create(request):
    print request.user.has_perm('task.add_task')
    if not request.user.has_perm('task.add_task'):
        return render(request, 'alert.html', {'msg': noperm + 'create task', 'type': 'error'})
    if request.method == 'POST':
        otcForm = AddTaskForm(request.POST, request.FILES)
        if otcForm.is_valid:
            print "data valid"
            data = otcForm.save(commit=False)
            data.author = request.user
            data.origin_dept = request.user.userprofile.dept
            data.save()
            otcForm.save()
            #TODO: Select redirect based on user status, as of now home
            return redirect('erp.views.home')
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
    if not request.user.has_perm('task.approve_task'):
        return render(request, 'alert.html', {'msg': noperm + 'approve task', 'type': 'error'})
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
            return redirect('task.views.pending_approval')
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
    if not request.user.has_perm('task.approve_task'):
        return render(request, 'alert.html', {'msg': noperm + 'approve task', 'type': 'error'})
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
            return redirect('task.views.pending_approval')
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
    return render(request, 'task/task.html', to_return)

def show_task_details(request, task_id):
    if not request.user.has_perm('task.view_task'):
        return render(request, 'alert.html', {'msg': noperm + 'view task', 'type': 'error'})
    task = get_object_or_404(Task, pk=task_id)
    comments = Comment.objects.filter(task__id = task_id)
    if task.destin_coord_acknowledged == True:
        ack = 'acknowledged'
    else:
        ack=''
    to_return = {
                'task': task,
                'comments': comments,
                'title': task.title,
                'ack': ack,
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

def pending_approval(request):
    if not request.user.has_perm('task.approve_task'):
        return render(request, 'alert.html', {'msg': noperm + 'aprove task', 'type': 'error'})
    destin_tasks = Task.objects.filter(destin_dept__id = request.user.get_profile().dept.id).filter(origin_core_aproved = True).filter(destin_core_aproved = False)
    origin_tasks = Task.objects.filter(origin_dept__id = request.user.get_profile().dept.id).filter(origin_core_aproved = False)
    print 'orig', origin_tasks
    print 'destin', destin_tasks
    to_return = {
                'destin_tasks': destin_tasks,
                'origin_tasks': origin_tasks,
                'title': 'Tasks pending for your approval',
                }
    return render(request, 'task/approval_list.html', to_return)

def task_update(request, task_id):
    if not request.user.has_perm('task.update_task_status'):
        return render(request, 'alert.html', {'msg': noperm + 'update task status', 'type': 'error'})
    task = get_object_or_404(Task, pk=task_id)
    tuForm = TaskUpdateForm(instance = task)
    cForm = CommentForm()
    print tuForm
    print cForm
    msg=''
    if request.method == 'POST':
        tuForm = TaskUpdateForm(data = request.POST, instance = task)
        cForm = CommentForm(data = request.POST)
        if tuForm.is_valid:
            tuForm.save()
            Cdata = cForm.save(commit = False)
            Cdata.author = request.user
            Cdata.task = task
            Cdata.save()
            msg = "Successfully updated task status"
            tuForm = TaskUpdateForm(instance = task)
            cForm = CommentForm()
            return redirect(show_task_details, task_id = task.id)
        else:
            print "didnt validate"
    else:
        tuForm = TaskUpdateForm(instance = task)
        cForm = CommentForm()
    to_return = {
                'title': 'Tasks',
                'tuForm': tuForm,
                'cForm': cForm,
                'msg': msg,
                }
    return render(request, 'task/update_task.html', to_return)

def task_acknowledge(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.destin_coord_acknowledged == False:
        task.destin_coord_acknowledged = True
        task.time_destn_coord_acknowledged = dt.datetime.now()
        task.save()
        msg = 'Task Acknowledged'
    else:
        msg = 'acknowledged'
    to_return = {
                'msg': msg,
                'task': task,
                'title': 'Tasks'
                }
    return redirect(show_task_details, task_id = task.id)

def task_comment(request, task_id):
    if not request.user.has_perm('task.comment_task'):
        return render(request, 'alert.html', {'msg': noperm + 'comment task', 'type': 'error'})
    task = get_object_or_404(Task, pk=task_id)
    cForm = CommentForm()
    print cForm
    msg=''
    if request.method == 'POST':
        cForm = CommentForm(data = request.POST)
        if cForm.is_valid:
            Cdata = cForm.save(commit = False)
            Cdata.author = request.user
            Cdata.task = task
            Cdata.save()
            msg = "Commented"
            cForm = CommentForm()
            return redirect(show_task_details, task_id = task.id)
        else:
            print "didnt validate"
    else:
        cForm = CommentForm()
    to_return = {
                'title': 'Tasks',
                'cForm': cForm,
                'msg': msg,
                }
    return render(request, 'task/update_task.html', to_return)