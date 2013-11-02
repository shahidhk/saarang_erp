from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from erp.models import Department, SubDepartment
from events.models import Event
# Create your models here.
class UserProfile(models.Model):
    status_choices=(
        ('webops', 'WebOpsCoord'),
        ('sec', 'Secretary'),
        ('core', 'Core'),
        ('coord', 'Co-ordinator'),
    )
    '''
        Define extra details needed for User other than default django fields
    '''
    #Username should be roll number
    user = models.OneToOneField(User)
    status = models.CharField(choices=status_choices, max_length=20)
    nick = models.CharField(max_length=60, null=True, blank=True)
    saarang_email = models.EmailField(max_length=100, blank=True, null=True)
    avatar = models.ImageField("Profile Pic", upload_to="avatars/", blank=True, null=True)
    post_count = models.IntegerField(default=0, null=True)
    dept = models.ForeignKey(Department, related_name='user_department', null=True, blank=True)
    sub_dept = models.ForeignKey(SubDepartment, related_name='user_sub_department', null=True, blank=True)
    events = models.ManyToManyField(Event, related_name='user_events', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    mobile = models.BigIntegerField(max_length=10, default=0)
    mobile_home = models.BigIntegerField(max_length=10,  blank=True, null=True)
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

post_save.connect(create_user_profile, sender=User, dispatch_uid='autocreate_nuser')