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
from random import *
from django.contrib import messages
import string, json

def auto_id(user_id):
    base = 'SA14W'
    num = "{0:0>5d}".format(user_id)
    sid = base + num
    return sid

@dajaxice_register
def modify_data(request, form):
    data=deserialize_form(form)
    dajax=Dajax()
    try:
        user = SaarangUser.objects.get(pk=int(data['user_id']))
        user.desk_id = data['desk_id']
        user.name = data['name']
        user.college = data['college']
        user.city = data['city']
        user.mobile = data['mobile']
        user.gender = data['gender']
        user.save()
        dajax.script("""$('#alert-user').show();$('#alert-user').html('<h3>User saved successfully, Please proceed to next user</h3>').attr('class','alert alert-success');clearForm();""")
    except:
        user = SaarangUser()
        user.desk_id = data['desk_id']
        user.name = data['name']
        user.email = data['email']
        user.college = data['college']
        user.city = data['city']
        user.mobile = "%0000000010d"%int(data['mobile'])
        user.gender = data['gender']
        user.save()
        user.saarang_id = auto_id(user.pk)
        characters = string.ascii_letters + string.punctuation  + string.digits
        password =  "".join(choice(characters) for x in range(randint(8, 16)))
        user.password = password
        user.activate_status = 2
        user.save()
        try:
            mail.send(
                [user.email], template='email/main/activate_confirm',
                context={'saarang_id':user.saarang_id, 'password':user.password}
            )
        except:
            pass
        dajax.script("""$('#alert-user').show();$('#alert-user').html('<h3>New user registered. Proceed to next user</h3>').attr('class','alert alert-success');clearForm();""")
    dajax.script("""$('#user_id').val('')""")
    return dajax.json()