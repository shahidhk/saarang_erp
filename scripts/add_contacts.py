from events.models import Event
from django.contrib.auth.models import User

def update_contacts():
    events = Event.objects.all()
    for event in events:
        text = '<p>For futher queries, contact <a href="mailto:'+event.email+ '">' + event.email + '</a></p><br/><p><b>Coordinators:</b></p><p><ol>'
        for user in event.user_events.all():
            coord = User.objects.get(pk=user.user_id)
            text += '<li>' + coord.first_name +'<br/>'+str(coord.userprofile.mobile)+'</li>'
        text+='</ol></p>'
        event.contacts = text
        event.save()
        print event.long_name, 'saved'
