# Register the data to be shown in admin page
from django.contrib import admin
from forum.models import *

admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)