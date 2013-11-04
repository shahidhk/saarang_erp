from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^$', 'registration.views.list_users', name='saarang_users'),
    url(r'^(?P<user_id>\d+)/$', 'registration.views.show_user', name='show_user'),
    url(r'^add/$', 'registration.views.add_user', name='add_user'),
    
    )
