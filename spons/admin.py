from django.contrib import admin

from models import SponsImageUpload

class SponsImageUploadAdmin(admin.ModelAdmin):
    list_display=('title', 'sponsor_link', 'logo', 'timestamp', 'uploaded_by')
    search_fields = ['title', 'sponsor_link']

admin.site.register(SponsImageUpload, SponsImageUploadAdmin)