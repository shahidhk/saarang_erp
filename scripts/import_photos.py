# Script to import photos of every user in ERP from CCW DATABASE
#Link: http://photos.iitm.ac.in/byroll.php?roll=ED12B031
from django.contrib.auth.models import User
import urllib

print "Getting ready to import....."
users = User.objects.all()
print 'Users loaded from DB'

def get_photos():
    for user in users:
        print 'Trying ',user.username,'..........'
        try:
            print 'http://photos.iitm.ac.in/byroll.php?roll='+user.username.upper()
            urllib.urlretrieve('http://photos.iitm.ac.in/byroll.php?roll='+user.username.upper(), 'media/avatars/'+str(user.username)+'.jpg')
            user.userprofile.avatar = 'avatars/'+str(user.username)+'.jpg'
            user.save()
            print user.username.upper(), ' saved'
        except Exception, e:
            print e.message, user.username, ' failed'
    print 'Completed!!!!!'

def update_db():
    for user in users:
        prof = user.get_profile()
        # prof.avatar
        # Have to comlete adding Image