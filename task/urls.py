from django.conf.urls import patterns, url

urlpatterns = patterns('',
    
    url(r'^$', 'task.views.index', name='index'),
    url(r'^add/$', 'task.views.origin_task_create', name='newtask'),

)
