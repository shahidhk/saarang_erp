from django.db import models

from erp.models import SubDepartment

class Event(models.Model):
    name = models.CharField(max_length=50)
    sub_dept = models.ForeignKey(SubDepartment, related_name='parent_department')
    google_group = models.CharField(max_length=200,blank=True,null=True)
    CATEGORY_CHOICES = (
        ('onsite', 'Onsite'),
        ('online', 'Online'),
        ('pre_reg', 'Pre registerd'),
        )
    registration_info = models.TextField(max_length=2000,blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50,blank=True)
    event_format = models.TextField(max_length=3000,blank=True,null=True)
    about = models.TextField(max_length=3000,blank=True,null=True)
    faqs = models.ManyToManyField('FAQ',related_name='event_faq',blank=True,null=True)
    FAQs = models.TextField(max_length=5000,blank=True,null=True)
    prizes = models.TextField(max_length=3000,blank=True,null=True)
    def __unicode__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=1000)
