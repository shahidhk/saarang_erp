from events.models import Event
from django.contrib.auth.models import User

def add_contacts():
    events = Event.objects.all()
    for event in events:
        event.contacts='<p>For futher querries contact '+event.email+'</p><br/><strong>Coordinators</strong><br/>'
        for user in event.user_events.all():
            event.contacts+=user.user.get_full_name()+'<br/>'+str(user.mobile)+'<br/><br/>'
        event.save()

