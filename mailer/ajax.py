# For simple dajax(ice) functionalities
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from dajaxice.utils import deserialize_form
# For rendering templates
from django.template import RequestContext
from django.template.loader import render_to_string
# Decorators
from django.contrib.auth.decorators import login_required
from scripts.utility import show_alert
from post_office import mail
import json

from events.models import Event, EventRegistration
from django.contrib.auth.models import User
from registration.models import SaarangUser
from models import MailLog

@dajaxice_register(method="GET", name="mailer.test_get")
def hello(request):
    """
        Test dajax
    """
    dajax = Dajax()
    dajax.assign('#btn1', 'value', 'Click here!')

    show_alert(dajax, 'error', "There were some errors : please rectify them") # show alert
    
    return dajax.json()

@dajaxice_register
def dash(request):
    dajax = Dajax()
    dajax.add_css_class('#item_dash', 'active')
    dajax.add_css_class('#topbar_dash', 'active')

    html_content = render_to_string('mailer/home.html', {}, RequestContext(request))
    
    if html_content:
        dajax.assign("#content", "innerHTML", html_content)
    
    return dajax.json()

@dajaxice_register
def mail_events(request):
    dajax=Dajax()
    dajax.remove_css_class('#item_dash', 'active')
    dajax.add_css_class('#item_events', 'active')
    dajax.remove_css_class('#item_approval', 'active')

    events = request.user.userprofile.events.all()
    if request.user.userprofile.status == 'core':
        events = Event.objects.all()

    to_return={
        'events':events,
    }
    html_content = render_to_string('mailer/events.html', to_return, RequestContext(request))
    
    if html_content:
        dajax.assign("#content", "innerHTML", html_content)
    
    return dajax.json()

@dajaxice_register
def event_regns(request, event_id):
    dajax=Dajax()
    registrations = EventRegistration.objects.filter(event= Event.objects.get(pk=event_id))
    to_return={
        'event_id':event_id,
        'registrations':registrations,
    }
    html_content = render_to_string('mailer/event_regns.html', to_return, RequestContext(request))
    if html_content:
        dajax.assign("#registration_data", "innerHTML", html_content)

    return dajax.json()

@dajaxice_register
def send_individual_mail(request, user_id, event_id):
    dajax=Dajax()
    user = SaarangUser.objects.get(pk=user_id)
    event = Event.objects.get(pk=event_id)
    to_return={
        'event':event,
        'from_email':event.email,
        'to_email':user.email,
        'email_type':'single',
    }
    html_content = render_to_string('mailer/mail.html', to_return, RequestContext(request))
    if html_content:
        dajax.assign("#registration_data", "innerHTML", html_content)

    return dajax.json()

@dajaxice_register
def send_group_mail(request,event_id):
    dajax=Dajax()
    event=Event.objects.get(pk=event_id)
    to_return={
        'event':event,
        'from_email':event.email,
        'to_email': 'All '+event.long_name+' participants',
        'email_type':'group',
    }
    html_content = render_to_string('mailer/mail.html', to_return, RequestContext(request))
    if html_content:
        dajax.assign("#registration_data", "innerHTML", html_content)
    return dajax.json()

@dajaxice_register
def send_email(request, form):
    data=deserialize_form(form)
    dajax=Dajax()
    event = Event.objects.get(pk=data['event_id'])
    if data['email_type'] == 'single':
        new_mail = MailLog.objects.create(from_email=data['from_email'], \
            to_email=data['to_email'], subject=data['subject'], \
            body=data['body'], created_by=request.user)
        mail.send(
            [data['to_email']],data['from_email'],
            subject=data['subject'],
            html_message=data['body'],
        )
        to_return ={
            'mail': new_mail,
        }
        html_content = render_to_string('mailer/sent_preview.html', to_return, RequestContext(request))
        if html_content:
            dajax.assign("#registration_data", "innerHTML", html_content)
            show_alert(dajax, 'info', 'Your email has been sent!')
    elif data['email_type'] == 'group':
        email_list=[]
        event = Event.objects.get(pk=data['event_id'])
        registrations = EventRegistration.objects.filter(event= event)
        if event.is_team:
            for regn in registrations:
                for mem in regn.team.members.all():
                    email_list.append(mem.email)
                email_list.append(regn.participant.email)
        elif not event.is_team:
            for regn in registrations:
                email_list.append(regn.participant.email)
        email_list = list(set(email_list))

        to_string=json.dumps(email_list)
        new_mail = MailLog.objects.create(from_email=data['from_email'], \
            to_email=to_string, subject=data['subject'], \
            body=data['body'], created_by=request.user, needs_approval=True)
        
        to_return ={
        'msg':'Submitted for Core approval',
        'to_string':to_string,
        'mail': new_mail,
        }
        html_content = render_to_string('mailer/sent_preview.html', to_return, RequestContext(request))
        if html_content:
            dajax.assign("#registration_data", "innerHTML", html_content)
            show_alert(dajax, 'info', 'Your email has been submitted for core approval!')
            event_cores = User.objects.filter(userprofile__status='core').filter(userprofile__dept__name='events')
            event_core_email = list(set([core.email for core in event_cores]))
            mail.send(
                event_core_email, subject='Email for Approval: Saarang ERP',
                html_message = html_content,
            )

    return dajax.json()

@dajaxice_register
def approval_list(request):
    dajax=Dajax()
    mails=MailLog.objects.filter(needs_approval=True).filter(is_approved=False)
    dajax.remove_css_class('#item_dash', 'active')
    dajax.remove_css_class('#item_events', 'active')
    dajax.add_css_class('#item_approval', 'active')
    to_return ={
        'mails': mails,
    }
    html_content = render_to_string('mailer/approval_list.html', to_return, RequestContext(request))
    if html_content:
        dajax.assign("#content", "innerHTML", html_content)
    return dajax.json()

@dajaxice_register
def core_approve_email(request, mail_id):
    dajax=Dajax()
    email = MailLog.objects.get(pk=mail_id)
    email.is_approved=True
    email.save()
    mail.send(
        json.loads(email.to_email),email.from_email,
        subject=email.subject,
        html_message=email.body,
    )
    to_return ={
        'msg':'Email has been sent',
        'mail': email,
    }
    show_alert(dajax,'info', 'Email has been sent')
    html_content = render_to_string('mailer/sent_preview.html', to_return, RequestContext(request))
    if html_content:
        dajax.assign("#content", "innerHTML", html_content)
    return dajax.json()

@dajaxice_register
def loading_email(request):
    dajax=Dajax()
    show_alert(dajax, 'info', 'Please wait while the emails are being send')
    return dajax.json()
