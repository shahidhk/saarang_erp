from django.contrib import admin
from models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display=('q1','q2','q3','suggestion')

admin.site.register(Feedback, FeedbackAdmin)