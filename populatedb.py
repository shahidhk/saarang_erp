from django.contrib.auth.models import User, Group, Permission
from forum.models import Forum
from erp.models import Department, Event
from django.conf import settings

coordperm = ['add_post', 'add_topic', 'add_task', 'close_task', 'comment_task', 
	'update_task_status', 'view_task', 'change_userprofile']
coreperm = ['add_user', 'add_department', 'add_event', 'add_post', 'add_topic',
	'add_comment', 'add_task', 'approve_task', 'change_task', 'close_task', 
	'comment_task', 'view_task', 'add_userprofile', 'update_task_status','change_userprofile']
def populate():
	print 'Regarding Forum'
	print 'Creating Users...'
	for i in range(1,10):
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

	print 'For Task app'
	create_dept()

def create_dept():
	for i,j in settings.DEPARTMENTS:
		#Create Department
		dept = Department.objects.create(name=i, long_name=j, description='Description about '+j)
		dept.save()
		evt = Event.objects.create(name='event'+i, long_name= 'Event'+i, description= 'Descrtiption of Event', dept = Department.objects.get(name=i))
		evt.save()

		print j + ' created'
		for l in range(1,3):
			#Coord
			coord = User.objects.create_user('coord'+str(l)+i, 'coord'+str(l)+i+'@saarang.org','pass')
			coord.first_name = 'coordinator'+i
			coord.last_name = str(l)
			coord.groups.add(Group.objects.get(name='coord'))
			coord.save()
			coord.get_profile().status='coord'
			coord.get_profile().dept = Department.objects.get(name=i)
			coord.get_profile().event = Event.objects.get(name='event'+i)
			coord.get_profile().save()
			coord.save()
			#Core
			core = User.objects.create_user('core'+str(l)+i, 'core'+str(l)+i+'@saarang.org','pass')
			core.first_name = 'core'+i
			core.last_name = str(l)
			core.groups.add(Group.objects.get(name='core'))
			core.save()
			core.get_profile().status='core'
			core.get_profile().dept = Department.objects.get(name=i)
			core.get_profile().event = Event.objects.get(name='event'+i)
			core.get_profile().save()
			core.save()