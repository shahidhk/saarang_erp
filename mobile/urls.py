from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^login/$', 'mobile.views.login', name='mobile_login'),
    
    )
