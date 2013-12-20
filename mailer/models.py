from django.db import models

from django.contrib.auth.models import User
import json
# Create your models here.
class MailLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    from_email = models.EmailField(max_length=200, default='webadmin@saarang.org')
    to_email = models.CharField(max_length=5000)
    subject = models.CharField(max_length=500)
    body = models.CharField(max_length=10000)
    created_by = models.ForeignKey(User, related_name='email_by_user')
    needs_approval = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def get_recieptents_count(self):
        return len(json.loads(self.to_email))
