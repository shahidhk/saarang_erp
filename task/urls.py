from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^$', 'task.views.show_task', name='index'),
    #url(r'^(?P<task_id>\d+)/$', 'task.views.show_task', name='showtask'),
    url(r'^add/$', 'task.views.origin_task_create', name='newtask'),
    url(r'^ocoreapprove/(?P<task_id>\d+)/$', 'task.views.origin_core_approval', name='ocoreapprove'),

)
