from django.db import models
from registration.models import SaarangUser

class Feedback(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    q1 = models.IntegerField(max_length=1, default=1)
    q2 = models.IntegerField(max_length=1, default=1)
    q3 = models.IntegerField(max_length=1, default=1)
    q4 = models.IntegerField(max_length=1, default=1)
    suggestion = models.TextField(blank=True, null=True)

class College(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name + ', '+self.city

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    sent = models.BooleanField(default=False)
    sent_to = models.ForeignKey(SaarangUser, related_name='coupon_user', blank=True, null=True)