from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse

from forms import CreateItemForm,CreateMementoForm
from models import Item,Memento,EventRequest,TransportRequest,HospitalityRequest,ItemRequest
from events.models import Event

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

#Not completed yet
def update_item_list(request):
    print request.POST
    for item_id in dict(request.POST):
        try:
            item = Item.objects.get(id=int(item_id))
            if request.POST[item_id] == 'on':
                item.is_active = True
            else:
                item.is_active = False
            item.save()
        except:
            pass 
    return HttpResponseRedirect(reverse('list_items'))

def update_memento_list(request):
    for memento_id in dict(request.POST):
        try:
            memento = Memento.objects.get(id=int(memento_id))
            print memento
            if request.POST[item_id] == 'on':
                memento.is_active = True
            else:
                memento.is_active = False
            memento.save()
        except:
            pass 
    return HttpResponseRedirect(reverse('list_mementos'))

def event_request(request,eventId):
    item_list = Item.objects.filter(is_active=True) 
    item_list_all = Item.objects.all()
    event=Event.objects.get(id=int(eventId))
    try:
        event_request = EventRequest.objects.get(event=event)
    except:
        hospi_request = HospitalityRequest.objects.create(accomodation_cost=0,refreshment_cost=0,number_of_people=0)
        trans_request = TransportRequest.objects.create(cost=0,number_of_people=0)
        item_to_save = ''
        for item in item_list_all:
            item_store=str(item.id)+'='+str(0)+';'
            item_to_save+=item_store
        item_request = ItemRequest.objects.create(item_request=item_to_save)
        event_request = EventRequest.objects.create(event=event,fr_request=item_request,hospi_request=hospi_request,trans_request=trans_request)
    item_request = event_request.fr_request
    item_count_list=[]
    item_list_comp = item_request.item_request
    for item in item_list_comp.split(';'):
        try:
            item_n = Item.objects.get(id=item.split('=')[0])
            if item_n.is_active:
                print item_n
                print item.split('=')[1]
                item_count_list+=item.split('=')[1]
        except:
            pass
    item_list_final = zip(item_list,item_count_list)
    if request.method == 'POST':
        item_to_save=''
        item_total_cost=0
        for item in item_list_all:
            item_name = 'item_'+str(item.id)
            try:
                item_count = int(request.POST[item_name])
            except:
                item_count = 0
            item_total_cost+=item_count*item.cost
            item_store=str(item.id)+'='+str(item_count)+';'
            item_to_save+=item_store

        acc_cost = request.POST['acc_cost']
        ref_cost = request.POST['ref_cost']
        acc_num = request.POST['acc_num']
        acc_comments = request.POST['acc_comments']
        trans_cost = request.POST['trans_cost']
        trans_number = request.POST['trans_number']
        trans_comments = request.POST['trans_comments']

        item_request = event_request.fr_request
        hospi_request = event_request.hospi_request
        trans_request = event_request.trans_request


        item_request.item_request = item_to_save
        item_request.total_cost = item_total_cost
        item_request.save()
        print item_request.item_request
        hospi_request.accomodation_cost = int(acc_cost)
        hospi_request.refreshment_cost = int(ref_cost)
        hospi_request.number_of_people = int(acc_num)
        hospi_request.comments = acc_comments
        hospi_request.save()
        trans_request.cost = int(trans_cost)
        trans_request.number_of_people = int(trans_number)
        trans_request.comments = trans_comments
        trans_request.save()
        event_request.save()
        return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

    to_return={
        'list':item_list_final,
        'eventId':eventId,
        'event_request':event_request,
    }

    return render(request, 'finance/event_request.html', to_return)

def event_misc_request(request,eventId):
    try:
        event_request = EventRequest.objects.get(event=eventId)
    except:
        event_request = EventRequest.objects.create(event=eventId)
    event_request.misc = request.POST['misc']
    event_request.save()
    return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

