from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
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
    url(r'^forum/', include('forum.urls')),

	url(r'^login/', 'erp.views.login_user', name='login'),
	url(r'^logout/', 'erp.views.logout_user', name='logout_user'),
	url(r'^page/', 'erp.views.page', name='page'),
)

urlpatterns += staticfiles_urlpatterns()