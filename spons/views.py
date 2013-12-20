# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.contrib import messages

from forms import AddLogoForm
from models import SponsImageUpload

def add_logo(request):
    form = AddLogoForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request,'Image successfully saved')
        HttpResponseRedirect(reverse('add_logo'))
    all_images = SponsImageUpload.objects.all()
    to_return = {
        'form':form,
        'list':all_images,
    }
    return render(request, 'spons/add_logo.html', to_return)
