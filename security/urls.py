from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # For mainsite
    url(r'^$', 'security.views.online', name='security_online'),
    url(r'^offline/$', 'security.views.home', name='security_home'),
    
    )
