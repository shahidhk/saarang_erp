from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class UserProfile(models.Model):
    #Username should be roll number
    user=models.OneToOneField(User)
    avatar = models.ImageField("Profile Pic", upload_to="avatars/", blank=True, null=True)
    post_count = models.IntegerField(default=0)
    department = models.CharField(max_length=60, choices=settings.DEPARTMENTS, blank=True)
    event=models.CharField(max_length=60, choices=settings.EVENTS)
    dob = models.DateField()
    mobile = models.IntegerField(max_length=10)
    mobile_home = models.IntegerField(max_length=10, null=True)
    facebook = models.URLField(null=True)
    hostel = models.CharField(max_length=60, choices=settings.HOSTELS, blank=True)
    room = models.IntegerField(max_length=4)
    #genfield = models.CharField(max_length=100,null=True)

    class Meta:
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfiles')

    def __unicode__(self):
        return unicode(self.user.username)
