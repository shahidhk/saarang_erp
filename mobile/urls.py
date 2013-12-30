from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^push/$', 'mobile.views.push', name='mobile_push'),
    url(r'^send_push/$', 'mobile.views.push_send', name='mobile_push_send'),

    url(r'^login/$', 'mobile.views.login', name='mobile_login'),
    url(r'^register/$', 'mobile.views.register', name='mobile_register'),
    
    )
