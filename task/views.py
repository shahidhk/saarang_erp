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
from task.forms import AddTaskForm

def origin_task_create(request):
    if request.method == 'POST':
        otcForm = AddTaskForm(request.POST)
        otcForm.save(commit=False)
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