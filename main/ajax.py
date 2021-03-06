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
import json, re, base64
import datetime as dt
from events.models import Event, EventRegistration
from django.contrib.auth.models import User
from registration.models import SaarangUser
from registration.views import auto_id
from models import College

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@dajaxice_register
def process_login(request, form):
    data=deserialize_form(form)
    dajax = Dajax()
    try:
        user = SaarangUser.objects.get(email=data['email'])
        if user.password == data['password']:
            if user.activate_status != 0:
                request.session['saaranguser_email'] = user.email
                user.last_login = dt.datetime.now()
                user.save()
                show_alert(dajax, 'info', 'Logged in')
                dajax.assign('#success-alert', 'innerHTML', '<center>Welcome ' + user.email)
                dajax.script("$('#registration').hide();$('#success-alert').show();")
                dajax.script("var msg='success';var user='"+user.email+"'; parent.postMessage([msg, user], 'http://saarang.org');")
            else:
                show_alert(dajax, 'warning', 'Please click on the link sent to your email to activate your account!')
        else:
            show_alert(dajax, 'error', 'Did you mis-spell your password?')
    except:
        show_alert(dajax, 'warning', 'Is your email id correct?')
    dajax.assign('#signin_button', 'value', 'Try again?')
    dajax.remove_css_class('#signin_button', 'btn-warning')
    return dajax.json()

@dajaxice_register
def new_user(request, form):
    data = deserialize_form(form)
    print data
    dajax = Dajax()
    if re.match(r'[^@]+@[^@]+\.[^@]+', data['email']):
        try:
            user=SaarangUser.objects.get(email=data['email'])
            show_alert(dajax,'info', 'You are already registered at Saarang')
        except:
            if re.match(r'^\d{10}$', data['mobile']):
                if data['password'] == data['repassword'] and data['password'] !='':
                    mail.send(
                        [data['email']], template='email/main/register_activate',
                        context={'encoded_email':base64.b64encode(data['email']),}
                    )
                    new_user=SaarangUser.objects.create(email=data['email'], mobile=data['mobile'], password=data['password'])
                    new_user.saarang_id = auto_id(new_user.pk)
                    if data['college'] != '0':
                        college = College.objects.get(pk=data['college'])
                        new_user.college = college.name + ', ' + college.city
                    new_user.save()
                    try:
                        college = data['new_college_text']
                        mail.send(
                            ['webadmin@saarang.org', 'muhammedshahid.k@gmail.com'], data['email'],
                            template='email/main/add_college',
                            context={'name':data['email'], 'college':college,}
                            )
                    except:
                        pass
                    dajax.assign('#success-alert', 'innerHTML', '<center><strong>Registration successfull. Please click on the link sent to your email to activate your account</strong>')
                    dajax.script("$('#registration').hide();$('#success-alert').show();")
                else:
                    show_alert(dajax, 'error', 'Passwords does not match!')
            else:
                show_alert(dajax, 'error', 'Mobile number should be exactly 10 digits!')
    else:
        show_alert(dajax, 'error', 'Please enter a valid email!')
    return dajax.json()
