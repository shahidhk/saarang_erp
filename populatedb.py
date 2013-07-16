from django.contrib.auth.models import User, Group
from forum.models import Forum
from django.conf import settings

def populate():
	print 'Creating Users...'
	for i in range(1,10):
		dat = User.objects.create_user('ee13b00'+str(i),'ee12b0'+str(i)+'@saarang.org','pass')
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

	print 'Initialisation Complete!'