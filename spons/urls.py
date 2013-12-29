from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^add_logo/$', 'spons.views.add_logo', name='spons_add_logo'),
    url(r'^delete_logo/(?P<logo_id>\d+)/$', 'spons.views.delete_logo', name='spons_delete_logo'),
    url(r'^edit_logo/(?P<logo_id>\d+)/$', 'spons.views.edit_logo', name='spons_edit_logo'),

    url(r'^save_logo/(?P<logo_id>\d+)/$', 'spons.views.save_logo', name='spons_save_logo'),

)