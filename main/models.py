from django.db import models
from registration.models import SaarangUser

class Feedback(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    q1 = models.IntegerField(max_length=1, default=1)
    q2 = models.IntegerField(max_length=1, default=1)
    q3 = models.IntegerField(max_length=1, default=1)
    suggestion = models.TextField(blank=True, null=True)