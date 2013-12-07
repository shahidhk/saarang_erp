from django.conf.urls import patterns, include, url
from main.views import *


urlpatterns = patterns('',
    # Examples:
    url(r'^register/(?P<eventId>\d+)/(?P<emailId>\w+)/', 'main.views.register', name='register'),
    url(r'^register_team/(?P<eventId>\d+)/(?P<emailId>\w+)/(?P<teamId>\d+)/', 'main.views.register_team', name='register_team'),
    url(r'^list_teams/(?P<eventId>\d+)/(?P<emailId>\w+)/', 'main.views.list_teams', name='list_teams'),
    url(r'^main_profile_edit/(?P<emailId>\w+)', 'main.views.main_profile_edit', name='main_profile_edit'),
    url(r'^create_team/(?P<emailId>\w+)/(?P<eventId>\d+)/', 'main.views.create_team', name='create_team'),
    url(r'^band_details/(?P<eventId>\d+)/(?P<emailId>\w+)/(?P<teamId>\d+)/', 'main.views.band_details', name='band_details'),

)