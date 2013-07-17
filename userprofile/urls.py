from django.conf.urls import patterns, url

urlpatterns = patterns('',
   
   	url(r'^$', 'userprofile.views.profile', name='profile'),
	
)
