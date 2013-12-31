from django.contrib import admin

from models import Hostel, Room, HospiTeam, Allotment

class HospiTeamAdmin(admin.ModelAdmin):
    list_display=('team_sid', 'name', 'leader', 'accomodation_status')
    search_fields = ['team_sid', 'name', 'leader']

class AllotmentAdmin(admin.ModelAdmin):
    list_display = ('team', 'alloted_by', 'timestamp')
    search_fields = ['team', 'alloted_by']
    
admin.site.register(HospiTeam, HospiTeamAdmin)
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Allotment, AllotmentAdmin)
