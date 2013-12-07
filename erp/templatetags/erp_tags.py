from django import template

from django.conf import settings

register = template.Library()

def split(value, arg):
    """Split the string based on arg and return the list"""
    return value.split(arg)

register.filter('split', split)

def app_name(value):
    '''Return the first word if url is given'''
    if settings.SUB_URL:
        return value.split('/')[2]
    else:
        return value.split('/')[1]

register.filter('app_name', app_name)
