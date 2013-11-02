from django.db import models
# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    long_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    
    def __unicode__(self):
        return self.long_name

class SubDepartment(models.Model):
    dept = models.ForeignKey(Department, related_name='parent_dept')
    name = models.CharField(max_length=50, unique=True)
    long_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    def __unicode__(self):
        return self.long_name