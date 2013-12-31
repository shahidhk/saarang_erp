from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def hospi(request):
    if request.user.userprofile.status != 'core' and request.user.userprofile.dept.name != 'hospi':
        return render(request, 'alert.html', {'msg': 'You dont have permission'})    
    return render(request, 'chat/hospi.html', {})

@login_required
def events(request):
    if request.user.userprofile.status != 'core' and request.user.userprofile.dept.name != 'events':
        return render(request, 'alert.html', {'msg': 'You dont have permission'}) 
    return render(request, 'chat/events.html', {})

@login_required
def general(request):
    if request.user.userprofile.status != 'core' and request.user.userprofile.dept.name != 'events' and request.user.userprofile.dept.name != 'hospi':
        return render(request, 'alert.html', {'msg': 'You dont have permission'}) 
    return render(request, 'chat/general.html', {})