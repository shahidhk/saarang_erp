# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def home(request):

    return render(request, 'mailer/home.html', locals())