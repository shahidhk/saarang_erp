from django.contrib import admin

from models import Badge

class BadgeAdmin(admin.ModelAdmin):
    list_display=('timestamp', 'name', 'barcode', 'rockshow', 'popular_night')
    search_fields = ['name', 'barcode']

admin.site.register(Badge, BadgeAdmin)