from models import Transaction,Transaction_final,Ticket
from forms import CreateTicketForm,CreateTransactionForm,EditTicketForm
from userprofile.models import UserProfile
from signals import *
from django.contrib import messages

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory

# Create your views here.
@login_required
def create_ticket(request):
    to_return={}
    if request.method == 'POST':
        ticketForm = CreateTicketForm(request.POST)
        if ticketForm.is_valid():
            ticketForm.save()
            return HttpResponseRedirect(reverse('ticket_list'))
        else:
            print 'didn.t validate'
            return HttpResponseRedirect(reverse('ticket_list'))
    else:
        ticketForm = CreateTicketForm()
        to_return={
            'form':ticketForm,
            'action':  "",
            'title': "Add a new Ticket"
        }
    return render(request, 'ticket/create_ticket.html', to_return )

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    recieve_signal_print.send(sender=None)
    return render(request, 'ticket/ticket_list.html', locals())

@login_required
def edit_ticket(request,ticket_id):
    ticket = get_object_or_404(Ticket,id=ticket_id)
    to_return={}
    if request.method == 'POST':
        ticketForm = EditTicketForm(request.POST)
        if ticketForm.is_valid():
            ticket.ticket_name = ticketForm.cleaned_data['ticket_name']
            ticket.active = ticketForm.cleaned_data['active']
            ticket.save()
            return HttpResponseRedirect(reverse('ticket_list'))
        else:
            print 'didnt validate'
            return HttpResponseRedirect(reverse('ticket_list'))
    else:
        ticketForm = EditTicketForm(instance=ticket)
        to_return={
            'form':ticketForm,
            'action':  "",
            'title': "Edit Ticket"
        }
    return render(request, 'ticket/edit_ticket.html', to_return)

@login_required
def delete_ticket(request,ticket_id):
    ticket = get_object_or_404(Ticket,id=ticket_id)
    ticket.delete()
    return HttpResponseRedirect(reverse('ticket_list'))

@login_required
def new_transaction(request):
    tickets = Ticket.objects.filter(active=True)
    if request.method == 'POST':
        challan_number = request.POST['chno']
        if Transaction_final.objects.filter(challan_number=challan_number):
            messages.error(request,'Challan number already in use.')
            return HttpResponseRedirect(reverse('new_transaction'))
        cost = request.POST['ticketcost']
        coord = UserProfile.objects.get(user = request.user)
        transaction_final = Transaction_final(challan_number=challan_number,coord=coord,cost=cost)
        if request.POST.has_key('customerid'):
            customer_id = request.POST['customerid']
            customer_check = Transaction_final.objects.filter(customer_id=customer_id)
            print customer_check
            print '------------'
            ticket_list_show=[]
            for ticket_id in dict(request.POST)['ticketid']:
                ticket_list_show.append(Ticket.objects.get(id=int(ticket_id)).ticket_show)
            if customer_check:
                for transaction_check in customer_check:
                    print transaction_check.ticket_final.all()
                    for item in transaction_check.ticket_final.all():
                        print item.ticket.ticket_name
                        print item.ticket.ticket_show
                        if item.ticket.ticket_show in ticket_list_show:
                            print "Already taken"
                            messages.error(request,'Discounted ticket already issued to the ID.')
                            return HttpResponseRedirect(reverse('new_transaction'))
            transaction_final.customer_id=customer_id
        transaction_final.save()
        for ticketid,ticket_count in zip(dict(request.POST)['ticketid'],dict(request.POST)['ticket_count']):
            ticketid = int(ticketid)
            ticket_count = int(ticket_count)
            transaction = Transaction.objects.create(ticket = Ticket.objects.get(id=ticketid),ticket_count=ticket_count)
            transaction_final.ticket_final.add(transaction)
        transaction_final.save()
        messages.success(request,'Transaction completed successfully.')
        return HttpResponseRedirect(reverse('new_transaction'))
    return render(request, 'ticket/new_transaction.html', locals())

@login_required
def transaction_list(request):
    transaction_list = Transaction_final.objects.all()
    return render(request, 'ticket/transaction_list.html', locals())

@login_required
def statistics(request):
    tickets = Ticket.objects.all()
    income = []
    ticket_c=[]
    tot_inc=0
    tot_count=0
    for tickt in tickets:
        count,inc=0,0
        ticket_in = Transaction.objects.filter(ticket = tickt)
        for tick in ticket_in:
            count += tick.ticket_count
            tot_count+=tick.ticket_count
            inc += (tick.ticket_count)*(tickt.cost)
            tot_inc+=(tick.ticket_count)*(tickt.cost)
        income.append(inc) 
        ticket_c.append(count)
    print income
    print ticket_c
    zip_data = zip(tickets,income,ticket_c)
    return render(request, 'ticket/statistics.html', locals())
