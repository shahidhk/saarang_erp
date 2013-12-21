from django.contrib import admin

from models import SaarangUser

class SaarangUserAdmin(admin.ModelAdmin):
    list_display=('saarang_id', 'email', 'name', 'mobile', 'gender')
    search_fields = ['email', 'saarang_id', 'name']

admin.site.register(SaarangUser, SaarangUserAdmin)