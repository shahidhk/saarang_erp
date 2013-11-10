# From Django
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'notifications.views.list_notifications', name='list_notifications'),
    # Examples:
 )