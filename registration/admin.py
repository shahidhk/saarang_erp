from django.contrib import admin

from models import SaarangUser, EmailList

class SaarangUserAdmin(admin.ModelAdmin):
    list_display=('timestamp','last_login',  'saarang_id', 'desk_id', 'email', 'name', 'mobile', 'gender')
    search_fields = ['email', 'saarang_id','desk_id', 'name']

admin.site.register(SaarangUser, SaarangUserAdmin)

class EmailListAdmin(admin.ModelAdmin):
    list_display=('pk', 'email')
    search_fields = ['email']
    
admin.site.register(EmailList, EmailListAdmin)
