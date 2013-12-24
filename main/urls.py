from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='main_home'),
    url(r'^register/(?P<eventId>\d+)/(?P<emailId>.+)/$', 'main.views.register', name='register'),
    url(r'^register/csrf/$', 'main.views.get_csrf', name='get_csrf'),
    url(r'^register_team/(?P<eventId>\d+)/(?P<emailId>.+)/(?P<teamId>\d+)/$', 'main.views.register_team', name='register_team'),
    url(r'^list_teams/(?P<eventId>\d+)/(?P<emailId>.+)/$', 'main.views.list_teams', name='list_teams'),
    url(r'^register/new/$', 'main.views.new_profile', name='register_new_user'),
    url(r'^create_team/(?P<emailId>.+)/(?P<eventId>\d+)/$', 'main.views.create_team', name='create_team'),
    url(r'^band_details/(?P<eventId>\d+)/(?P<emailId>.+)/(?P<teamId>\d+)/$', 'main.views.band_details', name='band_details'),

    url(r'^login/$', 'main.views.login', name='main_login'),
    url(r'^logout/$', 'main.views.logout', name='main_logout'),
    url(r'^check/$', 'main.views.check_login_status', name='main_check'),
    url(r'^profile/$', 'main.views.profile', name='main_profile'),


)