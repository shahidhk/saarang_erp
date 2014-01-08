from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^push/$', 'mobile.views.push', name='mobile_push'),
    url(r'^send_push/$', 'mobile.views.push_send', name='mobile_push_send'),

    url(r'^login/$', 'mobile.views.login', name='mobile_login'),
    url(r'^register/$', 'mobile.views.register', name='mobile_register'),
    url(r'^logout/$', 'mobile.views.logout', name='mobile_logout'),
    url(r'^register_event/$', 'mobile.views.register_event', name='mobile_register_event'),

    url(r'^set_session/$', 'mobile.views.set_session', name='mobile_set_session'),
    url(r'^get_session/$', 'mobile.views.get_session', name='mobile_get_session'),
	
	url(r'^register_team/$', 'mobile.views.register_team', name='mobile_register_team'),
    url(r'^barcode/$', 'mobile.views.mobileregistration', name='mobileregistration'),
    
    )
