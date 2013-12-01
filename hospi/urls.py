from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # For mainsite
    url(r'^$', 'hospi.views.home', name='hospi_home'),
    url(r'^add_members/$', 'hospi.views.add_members', name='hospi_add_members'),
    url(r'^del_member/(?P<team_id>\d+)/(?P<member_id>\d+)/$', 'hospi.views.delete_member', name='hospi_del_member'),
    url(r'^add_accomod/$', 'hospi.views.add_accomodation', name='hospi_add_accomodation'),

    # For ERP
    url(r'^admin/$', 'hospi.views.list_registered_teams', name='hospi_list_registered_teams'),


    
    )
