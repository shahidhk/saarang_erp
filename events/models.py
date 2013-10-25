from django.db import models

from erp.models import SubDepartment

class Event(models.Model):
    name = models.CharField(max_length=50, unique=True)
    sub_dept = models.ForeignKey(SubDepartment, related_name='parent_department', default=name)
    long_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1500)
    google_group = models.CharField(max_length=200)
    CATEGORY_CHOICES = (
        ('onsite', 'Onsite'),
        ('online', 'Online'),
        ('pre_reg', 'Pre registerd'),
        )
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    ideation = models.TextField(max_length=1500)
    spons_writeup = models.TextField(max_length=1500)
    publicity_writeup = models.TextField(max_length=1500)
    hospi_writeup = models.TextField(max_length=1500)
    format_rules = models.TextField(max_length=1500)
    inter_dept_rels = models.TextField(max_length=1500)
    prev_data = models.FileField(upload_to = 'attachments', blank=True, null=True)

    def __unicode__(self):
        return self.long_name