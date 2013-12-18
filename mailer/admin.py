from django.contrib import admin

from models import MailLog

def get_message_preview(instance):
    return (u'{0}...'.format(instance.body[:25]) if len(instance.body) > 25
            else instance.body)

class MailLogAdmin(admin.ModelAdmin):
    list_display = ('subject', 'from_email', 'to_email','timestamp',  get_message_preview, 'created_by' ,'needs_approval', 'is_approved')

admin.site.register(MailLog, MailLogAdmin)