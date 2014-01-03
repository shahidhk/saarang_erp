from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # For mainsite
    url(r'^$', 'security.views.home', name='security_home'),
    
    )
