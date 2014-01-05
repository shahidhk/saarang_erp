from django.db import models

# Create your models here.
class SaarangUser(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    saarang_id = models.CharField(max_length=20)
    desk_id = models.CharField(max_length=20, default='SA14W00')
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=100)
    mobile = models.BigIntegerField(max_length=10)
    city = models.CharField(max_length=100)
    fb_id = models.CharField(max_length=50)
    friend_list = models.TextField(max_length=1000)
    college = models.CharField(max_length=150)
    college_id = models.CharField(max_length=50)
    fb_token = models.TextField(max_length=1000)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    ACTIVATION_CHOICES = (
        ('0','Activation email sent'),
        ('1','Activated'),
        ('2','Profile completed'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    activate_status = models.IntegerField(choices = ACTIVATION_CHOICES, default=0, blank=True, null=True) #New field with choices as ACTIVATION_CHOICES
    password = models.CharField(max_length=128)
    accomod_is_confirmed = models.BooleanField(default=False)
    def __unicode__(self):
        return self.email

    def profile_is_complete(self):
        if (self.name and len(str((self.mobile)))==10 and self.gender and self.college):
            return True
        else:
            return False


class EmailList(models.Model):
    email = models.EmailField(max_length=100)
    def __unicode__(self):
        return self.email

    def get_users_count(self):
        return len(self.objects.all())