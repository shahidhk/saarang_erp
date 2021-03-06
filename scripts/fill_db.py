from django.contrib.auth.models import User, Group, Permission
from erp.models import Department, SubDepartment
import xlrd
from forum.models import Forum
from erp.models import Department
from events.models import Event
from django.conf import settings
from userprofile.models import UserProfile

book = xlrd.open_workbook('scripts/erp_users.xls')
coordperm = ['add_post', 'add_topic', 'add_task', 'close_task', 'comment_task', 
	'update_task_status', 'view_task', 'change_userprofile']
coreperm = ['add_user', 'add_department', 'add_subdepartment', 'add_event', 'add_post', 'add_topic',
	'add_comment', 'add_task', 'approve_task', 'change_task', 'close_task', 
	'comment_task', 'view_task', 'add_userprofile', 'update_task_status','change_userprofile']
def populate():
	print 'Regarding Forum'
	print 'Creating Users...'
	for i in range(1,3):
		dat = User.objects.create_user('ee13b00'+str(i),'ee12b00'+str(i)+'@saarang.org','pass')
		dat.save()
		print 'ee13b00'+ str(i)+ ' '+'created'

	print 'Creating Forums...'
	for i,j in settings.DEPARTMENTS:
		dept = Forum.objects.create(title=j, department=i)
		dept.save()
		print j + ' Forum created'

	print 'Creating Groups...'
	for i in ['Core', 'Coord', 'Convenor']:
		grp = Group.objects.create(name=i)
		print i +' group created'
		# TODO: Add permissions to groups

	print 'Initialisation Complete!'
	print 'Adding permissions'
	coregrp = Group.objects.get(name='core')
	for perm in coreperm:
		coregrp.permissions.add(Permission.objects.get(codename=perm))
	coregrp.save()

	coordgrp = Group.objects.get(name='coord')
	for perm in coordperm:
		coordgrp.permissions.add(Permission.objects.get(codename=perm))
	coordgrp.save()

	
def add_dept():
    sheet = book.sheet_by_name('departments')
    # (name, long_name)
    dept = zip(sheet.col_values(1),sheet.col_values(0))
    for n, ln in dept:
        print n, ln
        obj = Department.objects.create(name=n, long_name=ln, description="Description for "+ln)
        obj.save()

def add_subdept():
    sheet = book.sheet_by_name('subdepartments')
    data = zip(sheet.col_values(0),sheet.col_values(2),sheet.col_values(1))
    for d, sd, lsd in data:
        print d, sd, lsd
        obj = SubDepartment.objects.create(dept=Department.objects.get(name=d), name=sd, long_name=lsd, description="Description for "+lsd)
        obj.save()

def add_cores():
    sheet = book.sheet_by_name('cores')
    # (Name, nick, dept, email, mobile, saarang email, username, pass)
    data = zip (sheet.col_values(0),sheet.col_values(1),sheet.col_values(2),sheet.col_values(3),sheet.col_values(4),sheet.col_values(5),sheet.col_values(6),sheet.col_values(7))
    for n,ni,d,e,mo,se,un,pas in data:
        core = User.objects.create_user(un, e, pas)
        core.first_name = n
        core.groups.add(Group.objects.get(name='core'))
        core.save()
        profile = core.get_profile()
        profile.status = 'core'
        profile.nick = ni
        profile.mobile = int(mo)
        profile.dept = Department.objects.get(name=d)
        profile.saarang_email = se
        profile.save()
        core.save()
        print n+" added"

def add_mobile():
    sheet = book.sheet_by_name('cores')
    # (Name, nick, dept, email, mobile, saarang email, username, pass)
    data = zip (sheet.col_values(0),sheet.col_values(1),sheet.col_values(2),sheet.col_values(3),sheet.col_values(4),sheet.col_values(5),sheet.col_values(6),sheet.col_values(7))
    for n,ni,d,e,mo,se,un,pas in data:
        core = User.objects.get(username=un)
        print core
        profile = core.get_profile()
        print mo
        print int(mo)
        profile.mobile = int(mo)
        profile.save()
        core.save()

def add_coords():
    sheet = book.sheet_by_name('coords')
    # (name, roll num, email, mobile, dept, subdept)
    data = zip (sheet.col_values(0),sheet.col_values(1),sheet.col_values(2),sheet.col_values(3),sheet.col_values(4),sheet.col_values(5))
    for n,ro,e,mo,d,sd in data:
        coord = User.objects.create_user(ro, e, ro)
        coord.first_name = n
        coord.groups.add(Group.objects.get(name='coord'))
        coord.save()
        profile = coord.get_profile()
        profile.status = 'coord'
        profile.mobile = int(mo)
        profile.dept = Department.objects.get(name=d)
        profile.sub_dept = SubDepartment.objects.get(name=sd)
        profile.save()
        coord.save()
        print n+" added"

def add():
    populate()
    add_dept()
    add_subdept()
    add_cores()
    add_coords()

def add_events():
    sheet = book.sheet_by_name('events')
    data = zip(sheet.col_values(0),sheet.col_values(1),sheet.col_values(2))
    for d, ln, sd in data:
        print d, sd, ln
        obj = Event.objects.create(sub_dept=SubDepartment.objects.get(name=sd), name=ln)
        print ln
        obj.save()

def add_new_event_subdepts():
    sheet = book.sheet_by_name('eventssubdept')
    data = zip(sheet.col_values(0),sheet.col_values(2),sheet.col_values(1))
    for d, sd, lsd in data:
        print d, sd, lsd
        obj = SubDepartment.objects.create(dept=Department.objects.get(name=d), name=sd, long_name=lsd, description="Description for "+lsd)
        obj.save()

def add_new_events():
    sheet = book.sheet_by_name('new_events')
    data = zip(sheet.col_values(0),sheet.col_values(1),sheet.col_values(2))
    for sd, ev, le in data:
        print sd, ev, le
        try:
            subd = SubDepartment.objects.get(name=sd)
        except Exception, e:
            if e.message == 'Event matching query does not exist.':
                subd = SubDepartment.objects.create(name=sd)
            else:
                print 'other error', e.message
        try:
            obj = Event.objects.get(name='le')
        except Exception, e:
            if e.message == 'Event matching query does not exist.':
                obj = Event.objects.create(sub_dept=subd, long_name=ev, name=le)
            else:
                obj.sub_dept = subd
                obj.name = le
                obj.long_name = ev
        print le
        obj.save()

def add_events_coords():
    sheet = book.sheet_by_name('events_coords')
    # username, subdept, events
    data = zip(sheet.col_values(1),sheet.col_values(6),sheet.col_values(5))
    for uname, subd, e in data:
        user = User.objects.get(username=uname)
        print user.pk
        try:
            prof = UserProfile.objects.get(user_id=user.pk)
        except Exception, e:
            prof = UserProfile.objects.create(user_id=user.pk, status='coord', dept=Department.objects.get(name='events'))
        print user
        try:
            subdept = SubDepartment.objects.get(name=subd)
            ev = Event.objects.get(long_name=e)
        except Exception, e:
            raise e
        try:
            prof.sub_dept = subdept
            prof.events = ev
        except Exception, e:
            raise e
    prof.save()
    user.save()

# def add_refresh():
    