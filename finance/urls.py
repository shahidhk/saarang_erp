# From Django
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^add_item/$', 'finance.views.add_item', name='add_item'),
    url(r'^add_memento/$', 'finance.views.add_memento', name='add_memento'),
    url(r'^list_items/$', 'finance.views.list_items', name='list_items'),
    url(r'^list_mementos/$', 'finance.views.list_mementos', name='list_mementos'),
    url(r'^update_item_list/$', 'finance.views.update_item_list', name='update_item_list'),
    url(r'^update_memento_list/$', 'finance.views.update_memento_list', name='update_memento_list'),
    url(r'^event_request/(?P<eventId>\d+)/$', 'finance.views.event_request', name='event_request'),
    url(r'^event_misc_request/(?P<eventId>\d+)/$', 'finance.views.event_misc_request', name='event_misc_request'),
    url(r'^event_request_submit/(?P<eventId>\d+)/$', 'finance.views.event_request_submit', name='event_request_submit'),
    url(r'^misc_request/(?P<eventId>\d+)/(?P<miscId>\d+)/$', 'finance.views.misc_request', name='misc_request'),
    url(r'^approve_misc_request/(?P<eventId>\d+)/(?P<miscId>\d+)/$', 'finance.views.approve_misc_request', name='approve_misc_request'),
    url(r'^approve_item_request/(?P<itemId>\d+)/(?P<flag>\d+)/$', 'finance.views.approve_item_request', name='approve_item_request'),
    url(r'^approve_all_item_request/(?P<eventId>\d+)/(?P<flag>\d+)/$', 'finance.views.approve_all_item_request', name='approve_all_item_request'),
    url(r'^approve_hospi_request/(?P<itemId>\d+)/(?P<type_hospi>\d+)/(?P<flag>\d+)/$', 'finance.views.approve_hospi_request', name='approve_hospi_request'),
    url(r'^approve_all_hospi_request/(?P<eventId>\d+)/(?P<flag>\d+)/$', 'finance.views.approve_all_hospi_request', name='approve_all_hospi_request'),
    url(r'^event_request_revert/(?P<eventId>\d+)/$', 'finance.views.event_request_revert', name='event_request_revert'),
    url(r'^approve_prize_request/(?P<eventId>\d+)/(?P<counter>\d+)/(?P<flag>\d+)/$', 'finance.views.approve_prize_request', name='approve_prize_request'),
    url(r'^approve_all_prize_request/(?P<eventId>\d+)/(?P<flag>\d+)/$', 'finance.views.approve_all_prize_request', name='approve_all_prize_request'),
    # url(r'^faq/(?P<event_id>\d+)/$', 'events.views.event_faq', name='event_faq'),
    # url(r'^reg/(?P<event_id>\d+)/$', 'events.views.event_reg', name='event_reg'),
    # url(r'^format/(?P<event_id>\d+)/$', 'events.views.event_format', name='event_format'),
    # url(r'^prizes/(?P<event_id>\d+)/$', 'events.views.event_prizes', name='event_prizes'),
    # url(r'^register/$', 'events.views.register', name='register_event'),
    # url(r'^registrations/(?P<event_id>\d+)/$', 'events.views.list_registrations', name='event_registrations'),
    # url(r'^score/(?P<regn_id>\d+)/$', 'events.views.change_score', name='change_score'),
    # url(r'^addteam/$', 'events.views.add_team', name='add_team'),
    # url(r'^teams/$', 'events.views.list_teams', name='list_teams'),
    # url(r'^all_reg/$', 'events.views.list_all_registrations', name='list_all_registrations'),

)
