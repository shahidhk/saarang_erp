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
import json, datetime
from models import Badge

@dajaxice_register
def check_barcode(request, barcode):
    dajax=Dajax()
    try:
        badge = Badge.objects.get(barcode=barcode)
        if badge:
            if datetime.datetime.today().date().day is 11:
                if badge.rockshow == True:
                    return_message = badge.name + ' already entered'
                    return_type = 'error'
                else:
                    badge.rockshow = True
                    return_message = badge.name
                    return_type = 'success'
                    badge.save()
            elif datetime.datetime.today().date().day is 12:
                if badge.popular_night == True:
                    return_message = badge.name + ' already entered'
                    return_type = 'error'
                else:
                    badge.popular_night = True
                    return_message = badge.name
                    return_type = 'success'
                    badge.save()
            else:
                return_message = 'No show today'
                return_type = 'success'
        else:
            return_message = 'Barcode not found'
            return_type = 'error'
    except:
        return_message = 'Barcode not found'
        return_type = 'error'
    dajax.assign('#div_alert', 'innerHTML', "<h1 class='text-center'>"+return_message+"</h1>")
    dajax.remove_css_class('#div_alert', 'error' if return_type is 'success' else 'success')
    dajax.add_css_class('#div_alert', return_type)
    dajax.script('reset_page();')
    return dajax.json()