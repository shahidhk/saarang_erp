# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import mail as dmail
from models import MailLog
from registration.models import EmailList

from post_office import mail

@login_required
def home(request):

    return render(request, 'mailer/home.html', locals())

@login_required
def mass_mail(request):
    allowed = ['webops', 'events', 'publicity']
    if not request.user.userprofile.dept.name in allowed:
        to_return={
            'msg':'You dont have permission to send mass mail',
        }
        return render(request, 'alert.html', to_return)
    to_return={

    }
    return render(request, 'events/mass_mail.html', to_return)

@login_required
def send_mass_mail(request):
    allowed = ['webops', 'events', 'publicity']
    if not request.user.userprofile.dept.name in allowed:
        to_return={
            'msg':'You dont have permission to send mass mail',
        }
        return render(request, 'alert.html', to_return)
    data = request.POST.copy()
    new_mail = MailLog.objects.create(from_email=data['from_email'], \
        to_email='mass@saarang.org', subject=data['subject'], \
        body=data['body'], created_by=request.user)
    email_list=[]
    EL = EmailList.objects.all()
    for eml in EL:
        email_list.append(eml.email)
    mail.send(
        email_list,data['from_email'],
        subject=data['subject'],
        html_message=data['body'],
    )
    to_return ={
            'mail': new_mail,
        }
    messages.success(request, 'Email has been sent')
    return render(request, 'alert.html', to_return)