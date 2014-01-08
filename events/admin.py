from django.contrib import admin

from models import Event, EventRegistration, Team

class EventAdmin(admin.ModelAdmin):
    list_display = ('pk', 'long_name', 'email', 'is_team', 'registration_open')
    search_fields = ['long_name']

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['participant', 'event', 'timestamp', 'team']

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_sid', 'leader')
    search_fields = ['name', 'team_sid', 'leader']

admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
