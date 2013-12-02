# From Django
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

#E nable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'erp.views.home', name='home'),
    # url(r'^erp/', include('erp.foo.urls')),
    url(r'^newdept/$', 'erp.views.add_dept', name='add_dept'),
    url(r'^newsubdept/$', 'erp.views.add_subdept', name='add_subdept'),
    url(r'^newuser/$', 'erp.views.add_user', name='add_user'),
    url(r'^contacts/$', 'erp.views.contacts', name='contacts'),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^test/$', 'erp.views.test', name='add_dept'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Includes forum urls
    url(r'^forum/', include('forum.urls')),
    
    # Include urls from task
    url(r'^task/', include('task.urls')),

    # Include urls from events
    url(r'^event/', include('events.urls')),   

    # Include urls from ticket
    url(r'^ticket/', include('ticket.urls')),

    # Include urls from registration
    url(r'^registration/', include('registration.urls')),

    # Include urls from notifications
    url(r'^registration/', include('notifications.urls')),

    # Include urls from hospi
    url(r'^hospi/', include('hospi.urls')),

	url(r'^login/$', 'erp.views.login_user', name='login'),
	url(r'^logout/$', 'erp.views.logout_user', name='logout_user'),

    # Include Profile urls
    url(r'^profile/$', include('userprofile.urls')),


    # For media urls
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

# Renders static files
urlpatterns += staticfiles_urlpatterns()
