# From Django
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'events.views.list_events', name='list_events'),
    url(r'^new/$', 'events.views.add_event', name='add_event'),
    url(r'^details/(?P<event_id>\d+)/$', 'events.views.details_event', name='details_event'),
    
)