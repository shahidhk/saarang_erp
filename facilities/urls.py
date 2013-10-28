from django.conf.urls import patterns, include, url
from facilities import views
from facilities.models import user
from django.http import HttpResponse

urlpatterns= patterns('',
	url(r'^$', 'facilities.views.req',name='facilities_home'),
	url(r'/display', 'facilities.views.display',name='fac_display')
#	url(r'/(?P<user_id>\d+)/$',views.detail, name='detail'),
	)
