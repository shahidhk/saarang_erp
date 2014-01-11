from django.db import models

class Badge(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=20)
    rockshow = models.BooleanField(default=False)
    popular_night = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name