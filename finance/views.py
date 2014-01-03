from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse

import datetime

from forms import CreateItemForm,CreateMementoForm
from models import Item,Memento,EventRequest,TransportRequest,HospitalityRequest,ItemRequest,MiscRequest,Comments
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
    for item in Item.objects.all():
        try:
            item_val = request.POST[str(item.id)]
            item.is_active=True
            item.save()
        except:
            item.is_active=False
            item.save()
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
    item_count_list = []
    item_list_all = Item.objects.all()
    event=Event.objects.get(id=int(eventId))
    prize_list=[]
    try:
        event_request = EventRequest.objects.get(event=event)
        for i in event_request.prizes.split(';'):
            try:
                prize_list.append(int(i.split('=')[1]))
            except:
                break
    except:
        hospi_request = HospitalityRequest.objects.create(accomodation_cost=0,refreshment_cost=0,number_of_people=0)
        trans_request = TransportRequest.objects.create(cost=0,number_of_people=0)
        event_request = EventRequest.objects.create(event=event,hospi_request=hospi_request,trans_request=trans_request)
    for item in item_list:
        flag=0
        for request_item in event_request.item_request.all():
            if request_item.item == item:
                item_count_list.append(request_item.count)
                flag=1
                break
        if flag == 0:
            item_count_list.append(0)
    item_list_final = zip(item_list,item_count_list)
    item_all_approved=True
    hospi_all_approved = False
    prize_approved_all = True
    prize_approved=[]
    for i in event_request.prizes_approved:
        if i == '0':
            prize_approved_all = False
            break
    for i in event_request.prizes_approved:
        prize_approved.append(int(i))
    if event_request.hospi_request.approved_acc:
        if event_request.hospi_request.approved_ref:
            if event_request.trans_request.approved:
                hospi_all_approved = True
    for item in event_request.item_request.all():
        if not item.approved:
            item_all_approved = False
            break
    prize_list_final = zip(prize_list,prize_approved)
    if request.method == 'POST':
        item_to_save=''
        item_total_cost=0
        for item in item_list_all:
            item_name = 'item_'+str(item.id)
            try:
                item_count = int(request.POST[item_name])
            except:
                item_count = 0
            flag_request=0
            for request_item in event_request.item_request.all():
                flag_request=0
                if request_item.item == item:
                    request_item.count=item_count
                    request_item.save()
                    flag_request=1
                    break
            if flag_request==0:
                item_request = ItemRequest.objects.create(item=item,count=item_count)
                event_request.item_request.add(item_request)
        event_request.save()
        acc_cost = request.POST['acc_cost']
        ref_cost = request.POST['ref_cost']
        acc_num = request.POST['acc_num']
        acc_comments = request.POST['acc_comments']
        trans_cost = request.POST['trans_cost']
        trans_number = request.POST['trans_number']
        trans_comments = request.POST['trans_comments']

        hospi_request = event_request.hospi_request
        trans_request = event_request.trans_request


        hospi_request.accomodation_cost = int(acc_cost)
        hospi_request.refreshment_cost = int(ref_cost)
        hospi_request.number_of_people = int(acc_num)
        hospi_request.comments = acc_comments
        hospi_request.save()
        trans_request.cost = int(trans_cost)
        trans_request.number_of_people = int(trans_number)
        trans_request.comments = trans_comments
        trans_request.save()
        i=0
        prizes = ''
        prizes_approved=''
        while(1):
            prize_name = 'prize'+str(i+1)
            try:
                prize_amount = request.POST[prize_name]
            except:
                break
            prize = str(i+1)+'='+prize_amount+';'
            prizes_approved+='0'
            i+=1
            prizes+=prize
        event_request.number_of_prizes = i
        event_request.prizes = prizes
        event_request.prizes_approved=prizes_approved
        event_request.memento_number = int(request.POST['mem_number'])
        event_request.ppm_comments = request.POST['ppm_comments']
        event_request.save()
        return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

    to_return={
        'list':item_list_final,
        'eventId':eventId,
        'event_request':event_request,
        'prize_list_final':prize_list_final,
        'item_all_approved':item_all_approved,
        'hospi_all_approved':hospi_all_approved,
        'prize_approved_all':prize_approved_all,
    }

    return render(request, 'finance/event_request.html', to_return)

def event_request_submit(request,eventId):
    item_list = Item.objects.filter(is_active=True) 
    item_count_list = []
    item_list_all = Item.objects.all()
    event=Event.objects.get(id=int(eventId))
    prize_list=[]
    try:
        event_request = EventRequest.objects.get(event=event)
        for i in event_request.prizes.split(';'):
            try:
                prize_list.append(int(i.split('=')[1]))
            except:
                break
    except:
        hospi_request = HospitalityRequest.objects.create(accomodation_cost=0,refreshment_cost=0,number_of_people=0)
        trans_request = TransportRequest.objects.create(cost=0,number_of_people=0)
        event_request = EventRequest.objects.create(event=event,fr_request=item_request,hospi_request=hospi_request,trans_request=trans_request)
    for item in item_list:
        flag=0
        for request_item in event_request.item_request.all():
            if request_item.item == item:
                item_count_list.append(request_item.count)
                flag=1
                break
        if flag == 0:
            item_count_list.append(0)
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
            flag_request=0
            for request_item in event_request.item_request.all():
                flag_request=0
                if request_item.item == item:
                    request_item.count=item_count
                    request_item.save()
                    flag_request=1
                    break
            if flag_request==0:
                item_request = ItemRequest.objects.create(item=item,count=item_count)
                event_request.item_request.add(item_request)
        event_request.save()
        acc_cost = request.POST['acc_cost']
        ref_cost = request.POST['ref_cost']
        acc_num = request.POST['acc_num']
        acc_comments = request.POST['acc_comments']
        trans_cost = request.POST['trans_cost']
        trans_number = request.POST['trans_number']
        trans_comments = request.POST['trans_comments']

        hospi_request = event_request.hospi_request
        trans_request = event_request.trans_request


        hospi_request.accomodation_cost = int(acc_cost)
        hospi_request.refreshment_cost = int(ref_cost)
        hospi_request.number_of_people = int(acc_num)
        hospi_request.comments = acc_comments
        hospi_request.save()
        trans_request.cost = int(trans_cost)
        trans_request.number_of_people = int(trans_number)
        trans_request.comments = trans_comments
        trans_request.save()
        i=0
        prizes = ''
        prizes_approved=''
        while(1):
            prize_name = 'prize'+str(i+1)
            try:
                prize_amount = request.POST[prize_name]
            except:
                break
            prize = str(i+1)+'='+prize_amount+';'
            prizes_approved+='0'
            i+=1
            prizes+=prize
        event_request.number_of_prizes = i
        event_request.prizes = prizes
        event_request.prizes_approved=prizes_approved
        event_request.memento_number = int(request.POST['mem_number'])
        event_request.ppm_comments = request.POST['ppm_comments']

        event_request.submitted = True
        # event_request.total_cost = event_request.hospi_request.accomodation_cost + event_request.hospi_request.refreshment_cost + event_request.trans_request.cost + event_request.fr_request.total_cost
        event_request.timestamp = datetime.datetime.now()
        event_request.request_by = request.user.userprofile
        event_request.save()
        return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

def event_request_revert(request,eventId):
    event = Event.objects.get(id=int(eventId))
    event_request = EventRequest.objects.get(event=event)
    event_request.submitted = False
    event_request.save()
    return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

def event_misc_request(request,eventId):
    event = Event.objects.get(id=int(eventId))
    event_request = EventRequest.objects.get(event=event)
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        reason = request.POST['reason']
        request_by = request.user.userprofile

        misc_request = MiscRequest.objects.create(amount=amount,reason=reason,request_by=request_by)
        event_request.misc_list.add(misc_request)
        event_request.save()
    return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

def misc_request(request,eventId,miscId):
    misc_request=MiscRequest.objects.get(id=int(miscId))
    comment_list = misc_request.comments.all().order_by('-timestamp')
    if request.method =='POST':
        comment = request.POST['comment']
        comment = Comments.objects.create(comment=comment,by=request.user.userprofile)
        misc_request.comments.add(comment)
        misc_request.save()
        return HttpResponseRedirect(reverse('misc_request',args=(eventId,miscId,)))
    to_return={
        'misc_request':misc_request,
        'eventId':eventId,
        'comment_list':comment_list,
    }
    return render(request, 'finance/misc_request.html', to_return)

def approve_misc_request(request,eventId,miscId):
    misc_request = MiscRequest.objects.get(id=int(miscId))
    misc_request.approved = True 
    misc_request.save()
    comment = 'This request has been approved'
    comment = Comments.objects.create(comment=comment)
    misc_request.comments.add(comment)
    misc_request.save()
    return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

def approve_item_request(request,itemId,flag):
    item_request = ItemRequest.objects.get(id=int(itemId))
    if int(flag):
        item_request.approved = True
    else:
        item_request.approved = False
    item_request.save()
    return HttpResponseRedirect(reverse('event_request',args=(item_request.related_item_request.all()[0].event.id,)))

def approve_all_item_request(request,eventId,flag):
    event=Event.objects.get(id=int(eventId))
    event_request = EventRequest.objects.get(event=event)
    if int(flag):
        for item in event_request.item_request.all():
            item.approved = True
            item.save()
    else:
        for item in event_request.item_request.all():
            item.approved = False
            item.save()
    return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

def approve_hospi_request(request,itemId,type_hospi,flag):
    if int(type_hospi)==1:
        item_request = HospitalityRequest.objects.get(id=int(itemId))
        if int(flag):
            item_request.approved_acc = True
        else:
            item_request.approved_acc = False
        item_request.save()
        return HttpResponseRedirect(reverse('event_request',args=(item_request.hospi_request.all()[0].event.id,)))
    elif int(type_hospi)==2:
        item_request = HospitalityRequest.objects.get(id=int(itemId))
        if int(flag):
            item_request.approved_ref = True
        else:
            item_request.approved_ref = False
        item_request.save()
        return HttpResponseRedirect(reverse('event_request',args=(item_request.hospi_request.all()[0].event.id,)))
    elif int(type_hospi)==3:
        item_request = TransportRequest.objects.get(id=int(itemId))
        if int(flag):
            item_request.approved = True
        else:
            item_request.approved = False
        item_request.save()
        return HttpResponseRedirect(reverse('event_request',args=(item_request.trans_request.all()[0].event.id,)))

def approve_all_hospi_request(request,eventId,flag):
    event=Event.objects.get(id=int(eventId))
    event_request = EventRequest.objects.get(event=event)
    if int(flag):
        hospi_request = event_request.hospi_request
        trans_request = event_request.trans_request

        hospi_request.approved_acc = True
        hospi_request.approved_ref = True
        trans_request.approved = True
        hospi_request.save()
        trans_request.save()
    else:
        hospi_request = event_request.hospi_request
        trans_request = event_request.trans_request

        hospi_request.approved_acc = False
        hospi_request.approved_ref = False
        trans_request.approved = False
        hospi_request.save()
        trans_request.save()
    return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

def approve_prize_request(request,eventId,counter,flag):
    event_request = EventRequest.objects.get(event=int(eventId))
    prizes_approved = event_request.prizes_approved
    prizes_approved_new = ''
    for i,j in enumerate(prizes_approved):
        if i == int(counter):
            if int(flag):
                prizes_approved_new+='1'
            else:
                prizes_approved_new+='0'
        else:
            prizes_approved_new+=j
    event_request.prizes_approved=prizes_approved_new
    event_request.save()
    return HttpResponseRedirect(reverse('event_request',args=(eventId,)))

def approve_all_prize_request(request,eventId,flag):
    event_request = EventRequest.objects.get(event=int(eventId))
    prizes_approved = event_request.prizes_approved
    prizes_approved_new = ''
    for i,j in enumerate(prizes_approved):
        if int(flag):
            prizes_approved_new+='1'
        else:
            prizes_approved_new+='0'
    event_request.prizes_approved=prizes_approved_new
    event_request.save()
    return HttpResponseRedirect(reverse('event_request',args=(eventId,)))