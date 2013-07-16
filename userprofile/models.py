from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
# Create your models here.
class UserProfile(models.Model):
    '''
        Define extra details needed for User other than default django fields
    '''
    #Username should be roll number
    user = models.OneToOneField(User)
    nick = models.CharField(max_length=60, null=True)
    avatar = models.ImageField("Profile Pic", upload_to="avatars/", blank=True)
    post_count = models.IntegerField(default=0)
    department = models.CharField(max_length=60, choices=settings.DEPARTMENTS, blank=True, null=True)
    event = models.CharField(max_length=60, choices=settings.EVENTS, null=True)
    dob = models.DateField(blank = True, null=True)
    mobile = models.IntegerField(max_length=10, blank=True, null=True)
    mobile_home = models.IntegerField(max_length=10,  blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    hostel = models.CharField(max_length=60, choices=settings.HOSTELS, blank=True, null=True)
    room = models.IntegerField(max_length=4, blank=True, null=True)
    
    class Meta:
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfiles')

    def __unicode__(self):
        return unicode(self.user.username)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)