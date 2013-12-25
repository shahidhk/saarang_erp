from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^login/$', 'mobile.views.login', name='mobile_login'),
    url(r'^register/$', 'mobile.views.register', name='mobile_register'),
    
    )
