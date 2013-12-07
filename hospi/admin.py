from django.contrib import admin

from models import Hostel, Room
from events.models import Team

admin.site.register(Team)
admin.site.register(Hostel)
admin.site.register(Room)
