from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='main_home'),
    url(r'^register/(?P<eventId>\d+)/(?P<emailId>.+)/$', 'main.views.register', name='register'),
    url(r'^register_team/(?P<eventId>\d+)/(?P<emailId>.+)/(?P<teamId>\d+)/$', 'main.views.register_team', name='register_team'),
    url(r'^list_teams/(?P<eventId>\d+)/(?P<emailId>.+)/$', 'main.views.list_teams', name='list_teams'),
    url(r'^main_profile_edit/(?P<emailId>.+)/$', 'main.views.main_profile_edit', name='main_profile_edit'),
    url(r'^register/new/$', 'main.views.new_profile', name='register_new_user'),
    url(r'^create_team/(?P<emailId>.+)/(?P<eventId>\d+)/$', 'main.views.create_team', name='create_team'),
    url(r'^band_details/(?P<eventId>\d+)/(?P<emailId>.+)/(?P<teamId>\d+)/$', 'main.views.band_details', name='band_details'),
)