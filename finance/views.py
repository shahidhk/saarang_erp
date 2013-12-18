from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse

from forms import CreateItemForm,CreateMementoForm
from models import Item,Memento
def add_item(request):
    createitemForm = CreateItemForm(request.POST or None)
    if createitemForm.is_valid():
        createitemForm.save()
        return HttpResponseRedirect(reverse('list_items'))
    to_return = {
        'form':createitemForm,
    }
    return render(request, 'finance/createitem.html', to_return)

def add_memento(request):
    createmementoForm = CreateMementoForm(request.POST or None)
    if createmementoForm.is_valid():
        createmementoForm.save()
        return HttpResponseRedirect(reverse('list_mementos'))
    to_return = {
        'form':createmementoForm,
    }
    return render(request, 'finance/creatememento.html', to_return)

def list_items(request):
    item_list = Item.objects.all()
    print item_list
    to_return = {
        'list':item_list,
    }
    return render(request, 'finance/list_items.html', to_return)

def list_mementos(request):
    memento_list = Memento.objects.all()
    to_return = {
        'list':memento_list,
    }
    return render(request, 'finance/list_items.html', to_return)
