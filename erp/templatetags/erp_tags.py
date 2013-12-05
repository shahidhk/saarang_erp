from django import template

register = template.Library()

def split(value, arg):
    """Split the string based on arg and return the list"""
    return value.split(arg)

register.filter('split', split)

def app_name(value):
    '''Return the first word if url is given'''
    return value.split('/')[2]

register.filter('app_name', app_name)
