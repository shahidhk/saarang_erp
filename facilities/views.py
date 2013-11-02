from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from facilities.models import *
from django.contrib.auth import authenticate
from facilities.forms import *
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from userprofile.models import UserProfile
#def contact(request):
#	if request.method == 'POST':
#		form = ContactForm(request.POST)
#		if form.is_valid():
#			return HttpResponseRedirect('/thanks')
#	else:
#		form = ContactForm()
#		return render(request,'contact.html',{'form':form})
	
def req(request):
	return render(request,'base.html')

def trans(request):
	form=Transport_form()
	if request.method == 'POST':
		form = Transport_form(request.POST)
		nuform=Fac_Trans.objects.create()
		print request.POST
		if form.is_valid():
#			print form.cleaned_data['equip_date']
#			print form.cleaned_data['equip_time']
			return HttpResponseRedirect(reverse('facilities_home'))
		else:
			print "didnt validate"
	return render(request,'facilities/user.html',{'form':form,'form_heading':'Transport'})

def equip(request):
	form=Equipment_form()
	if request.method == 'POST':
		form = Equipment_form(request.POST)
		nuform=Fac_Equip()
		print request.POST
		if form.is_valid():
			equip_date = form.cleaned_data['equip_date']
			equip_time = form.cleaned_data['equip_time']
			nuform.user=request.user
			print request.user
			user = UserProfile.objects.get(user=request.user)
			nuform.dept=user.dept
#			equipment = FacilitiesEquip.objects.create(equip_date=equip_date)
			return HttpResponseRedirect(reverse('facilities_home'))
		else:
			print "didnt validate"
	return render(request,'facilities/user.html',{'form':form,'form_heading':'Equipment'})

def ip_request(request):
	form=Ip_form()
	if request.method == 'POST':
		form = Ip_form(request.POST)
		print request.POST
		if form.is_valid():
#			print form.cleaned_data['equip_date']
#			print form.cleaned_data['equip_time']
			return HttpResponseRedirect(reverse('facilities_home'))
		else:
			print "didnt validate"
	return render(request,'facilities/user.html',{'form':form,'form_heading':'IP request'})

def ven(request):
	form=Venue_form()
	if request.method == 'POST':
		form = Venue_form(request.POST)
		print request.POST
		if form.is_valid():
#			print form.cleaned_data['equip_date']
#			print form.cleaned_data['equip_time']
			return HttpResponseRedirect(reverse('facilities_home'))
		else:
			print "didnt validate"
	return render(request,'facilities/user.html',{'form':form,'form_heading':'Venue request form'})

def display(request):
	if request.method=='POST':
		form=venueform(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/Thanks/')
		else:
			print "didnt validate"
			form=venueform()
			return render(request,'facilities/user.html',{'form':form})
	
	else:
		form=venueform()
		return render(request,'facilities/user.html',{'form':form})
		
