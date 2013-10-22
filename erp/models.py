from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    long_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    
    def __unicode__(self):
        return self.long_name