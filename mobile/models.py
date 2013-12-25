from django.db import models
from registration.models import SaarangUser

class Device(models.Model):
    key = models.CharField(max_length=100)
    user = models.ForeignKey(SaarangUser, related_name='user_device')
    created = models.DateTimeField(auto_now_add=True)
    last_access = models.DateTimeField()
