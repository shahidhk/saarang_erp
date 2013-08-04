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

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Includes forum urls
    url(r'^forum/', include('forum.urls')),
    
    # Include urls from task
    url(r'^task/', include('task.urls')),

	url(r'^login/$', 'erp.views.login_user', name='login'),
	url(r'^logout/$', 'erp.views.logout_user', name='logout_user'),

    # Include Profile urls
    url(r'^profile/$', include('userprofile.urls')),

    # For media urls
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

# Renders static files
urlpatterns += staticfiles_urlpatterns()
