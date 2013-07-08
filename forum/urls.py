from django.conf.urls import patterns, url

urlpatterns = patterns('',
   
   	url(r'^$', 'forum.views.index', name='index'),
	url(r'^(?P<forum_id>\d+)/$', 'forum.views.show_forum', name='forum'),

    #Topic
    url(r'^topic/(?P<topic_id>\d+)/$', 'forum.views.show_topic', name='topic'),
    url(r'^(?P<forum_id>\d+)/topic/add/$', 'forum.views.add_topic', name='add_topic'),
    url(r'^topic/(?P<topic_id>\d+)/delete_posts/$', 'forum.views.delete_posts', name='delete_posts'),
    url(r'^topic/(?P<topic_id>\d+)/open_close/(?P<action>[c|o])/$', 'forum.views.open_close_topic', name='open_close_topic'),

    #Posts
    url(r'^(?P<topic_id>\d+)/post/add/$', 'forum.views.add_post', name='add_post'),
    url(r'^post/(?P<post_id>\d+)/$', 'forum.views.show_post', name='post'),
    url(r'^post/(?P<post_id>\d+)/edit/$', 'forum.views.edit_post', name='edit_post'),
    url(r'^post/(?P<post_id>\d+)/delete/$', 'forum.views.delete_post', name='delete_post'),
)
