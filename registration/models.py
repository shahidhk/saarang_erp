from django.db import models

# Create your models here.
class SaarangUser(models.Model):
    saarang_id = models.CharField(max_length=20)
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=100)
    mobile = models.BigIntegerField(max_length=10)
    fb_id = models.CharField(max_length=50)
    friend_list = models.TextField(max_length=1000)
    college = models.CharField(max_length=150)
    fb_token = models.TextField(max_length=1000)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    ACTIVATION_CHOICES = (
        ('0','Activation email sent'),
        ('1','Activated'),
        ('2','Profile completed'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    activate_status = models.IntegerField(choices = ACTIVATION_CHOICES) #New field with choices as ACTIVATION_CHOICES
    password = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name
