# From Django
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'events.views.list_events', name='list_events'),
    url(r'^new/$', 'events.views.add_event', name='add_event'),
    url(r'^details/(?P<event_id>\d+)/$', 'events.views.details_event', name='details_event'),
    url(r'^det/(?P<event_id>\d+)/$', 'events.views.event_det', name='event_det'),
    url(r'^about/(?P<event_id>\d+)/$', 'events.views.event_about', name='event_about'),
    url(r'^faq/(?P<event_id>\d+)/$', 'events.views.event_faq', name='event_faq'),
    url(r'^reg/(?P<event_id>\d+)/$', 'events.views.event_reg', name='event_reg'),
    url(r'^format/(?P<event_id>\d+)/$', 'events.views.event_format', name='event_format'),
    url(r'^prizes/(?P<event_id>\d+)/$', 'events.views.event_prizes', name='event_prizes'),

)