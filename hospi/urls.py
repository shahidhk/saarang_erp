from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # For mainsite
    url(r'^$', 'hospi.views.home', name='hospi_home'),
    url(r'^add_members/$', 'hospi.views.add_members', name='hospi_add_members'),
    url(r'^del_member/(?P<team_id>\d+)/(?P<member_id>\d+)/$', 'hospi.views.delete_member', name='hospi_del_member'),
    url(r'^add_accomod/$', 'hospi.views.add_accomodation', name='hospi_add_accomodation'),

    # For ERP
    url(r'^admin/$', 'hospi.views.list_registered_teams', name='hospi_list_registered_teams'),
    url(r'^admin/details/(?P<team_id>\d+)/$', 'hospi.views.team_details', name='hospi_team_details'),
    url(r'^admin/update/(?P<team_id>\d+)/$', 'hospi.views.update_status', name='hospi_update_status'),
    url(r'^admin/statistics/$', 'hospi.views.statistics', name='hospi_statistics'),
    url(r'^admin/add/$', 'hospi.views.add_hostel_rooms', name='hospi_add_hostel_rooms'),
    url(r'^admin/add/hostel/$', 'hospi.views.add_hostel', name='hospi_add_hostel'),
    url(r'^admin/add/room/$', 'hospi.views.add_room', name='hospi_add_room'),
    url(r'^admin/rooms/$', 'hospi.views.room_map', name='hospi_room_map'),
    url(r'^admin/hostel/(?P<hostel_id>\d+)/$', 'hospi.views.hostel_details', name='hospi_hostel_details'),
    url(r'^admin/room/(?P<room_id>\d+)/$', 'hospi.views.room_details', name='hospi_room_details'),
    url(r'^admin/all_teams/$', 'hospi.views.list_all_teams', name='hospi_list_all_teams'),
    url(r'^admin/add/team/$', 'hospi.views.add_team', name='hospi_add_team'),
    url(r'^admin/save/team/$', 'hospi.views.save_team', name='hospi_save_team'),
    url(r'^admin/check_in/(?P<team_id>\d+)/$', 'hospi.views.check_in_team', name='hospi_check_in_team'),
    url(r'^admin/check_in_mixed/$', 'hospi.views.check_in_mixed', name='hospi_check_in_mixed'),
    url(r'^admin/check_in_males/$', 'hospi.views.check_in_males', name='hospi_check_in_males'),
    url(r'^admin/check_in_females/$', 'hospi.views.check_in_females', name='hospi_check_in_females'),
    url(r'^admin/check_out/(?P<team_id>\d+)/$', 'hospi.views.check_out_team', name='hospi_check_out_team'),


    )
