from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^$', 'task.views.show_task', name='index'),
    #url(r'^(?P<task_id>\d+)/$', 'task.views.show_task', name='showtask'),
    url(r'^add/$', 'task.views.origin_task_create', name='newtask'),
    url(r'^ocoreapprove/(?P<task_id>\d+)/$', 'task.views.origin_core_approval', name='ocoreapprove'),
    url(r'^dcoreapprove/(?P<task_id>\d+)/$', 'task.views.destin_core_approval', name='dcoreapprove'),
    url(r'^details/(?P<task_id>\d+)/$', 'task.views.show_task_details', name='task_details'),
    url(r'^mytask/$', 'task.views.my_task', name='my_task'),
    url(r'^depttask/$', 'task.views.dept_task', name='dept_task'),
    url(r'^pending/$', 'task.views.pending_approval', name='pending'),
    url(r'^update/(?P<task_id>\d+)/$', 'task.views.task_update', name='task_update'),
    url(r'^acknowledge/(?P<task_id>\d+)/$', 'task.views.task_acknowledge', name='task_acknowledge'),
)
