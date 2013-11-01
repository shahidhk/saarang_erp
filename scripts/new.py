from erp.models import Department

In [4]: ev = Department.objects.get(name='events')

In [5]: u=[]

In [6]: users = User.objects.all()

In [7]: for user in users:
    if user.get_profile().dept==ev:
        u.append(user)




from django.contrib.auth.models import User

In [2]: fro erp.models import Department, SubDepartment
  File "<ipython-input-2-6f59f18ddd06>", line 1
    fro erp.models import Department, SubDepartment
          ^
SyntaxError: invalid syntax


In [3]: from erp.models import Department, SubDepartment

In [4]: from events.models import Event

In [5]: events = Events.objects.all()
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
/usr/local/lib/python2.7/dist-packages/django/core/management/commands/shell.pyc in <module>()
----> 1 events = Events.objects.all()

NameError: name 'Events' is not defined

In [6]: events = Event.objects.all()

In [7]: for event in events:
   ...:     
KeyboardInterrupt

subdepts = SubDepartment.objects.all()
eventdep = Department.objects.get(name='events')
subdepts = SubDepartment.objects.all().filter(dept=eventdep)
SubDepartment.objects.create(dept=eventdep,name='events', long_name='Events', description = 'Desc')
subby = SubDepartment.objects.get(name='events')
for event in events:
    event.sub_dept = subby
    event.save()
from userprofile.models import UserProfile
event_users = UserProfile.objects.all().filter(dept=Department.objects.get(name='events'))

for user in event_users:
    user.sub_dept = subby
    user.save()
SubDepartment.objects.filter(dept_id=2).delete()
fill_db.add_new_events_subdepts()
fill_db.add_new_events()