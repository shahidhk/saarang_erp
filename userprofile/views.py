from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from userprofile.models import UserProfile
from userprofile.forms import UserProfileForm, UserForm

@login_required
def profile(request):
    
    profile = request.user.get_profile()
    u = request.user
    form = UserProfileForm( instance = profile )
    uform = UserForm( instance = u )

    if request.method == 'POST':
        uform = UserForm(data = request.POST, instance = u)
        form=UserProfileForm(request.POST, instance=profile)
        if form.is_valid() and uform.is_valid():
            data=form.save(commit=False)
            data.user=request.user
            uform.save()
            data.save()
            
        else:
            for error in form.errors:
                pass
    else:
        pass
    
    return render(request, 'userprofile.html',{'form':form, 'uform':uform, 'username':request.user})
