from django.contrib import admin

from models import Device

class DeviceAdmin(admin.ModelAdmin):
    list_display=('user', 'key', 'created', 'last_access', 'is_active')
    search_fields = ['user', 'key']

admin.site.register(Device, DeviceAdmin)