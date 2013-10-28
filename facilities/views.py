from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from facilities.models import *
from django.contrib.auth import authenticate
from facilities.forms import *
from django.core.urlresolvers import reverse

#def contact(request):
#	if request.method == 'POST':
#		form = ContactForm(request.POST)
#		if form.is_valid():
#			return HttpResponseRedirect('/thanks')
#	else:
#		form = ContactForm()
#		return render(request,'contact.html',{'form':form})
	
def req(request):
	form=equipment()
	if request.method == 'POST':
		form = equipment(request.POST)
		print request.POST
		if form.is_valid():
			print form.cleaned_data['equip_date']
			print form.cleaned_data['equip_time']
			return HttpResponseRedirect(reverse('facilities_home'))
		else:
			print "didnt validate"
	return render(request,'facilities/user.html',{'form':form})

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
		
