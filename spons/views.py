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
    if not request.user.has_perm('manage_logo'):
        return render(request, 'alert.html', {'msg':'You dont have permission',})
    form = AddLogoForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        img = form.save(commit=False)
        img.uploaded_by = request.user
        img.save()
        messages.success(request,'Image successfully saved')
        HttpResponseRedirect(reverse('spons_add_logo'))
    all_images = SponsImageUpload.objects.all()
    to_return = {
        'form':form,
        'list':all_images,
    }
    return render(request, 'spons/add_logo.html', to_return)

def delete_logo(request, logo_id):
    if not request.user.has_perm('manage_logo'):
        return render(request, 'alert.html', {'msg':'You dont have permission',})
    logo=SponsImageUpload.objects.get(pk=logo_id)
    logo.delete()
    messages.success(request, 'Logo deleted successfully!')
    return redirect('spons_add_logo')