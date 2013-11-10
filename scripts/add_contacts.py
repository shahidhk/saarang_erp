from events.models import Event
from django.contrib.auth.models import User

def add_contacts():
    events = Events.objects.all()
    for event in events:
        event.contacts='<p>For futher querries contact'+events.email+'</p><br/>'
        for user in event.user_events.all():
            event.contacts+=user.name

