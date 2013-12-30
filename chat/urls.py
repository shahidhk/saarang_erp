from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^hospi/$', 'chat.views.hospi', name='chat_hospi'),
    url(r'^events/$', 'chat.views.events', name='chat_events'),
    url(r'^general/$', 'chat.views.general', name='chat_general'),
    

)