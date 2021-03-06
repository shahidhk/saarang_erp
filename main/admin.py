from django.contrib import admin
from models import Feedback, College, LastCoupon, Coupon

class FeedbackAdmin(admin.ModelAdmin):
    list_display=('timestamp','q1','q2','q3','q4', 'suggestion')

admin.site.register(Feedback, FeedbackAdmin)

class CollegeAdmin(admin.ModelAdmin):
    list_display=('pk', 'name', 'city')
    search_fields=['name','city']

admin.site.register(College, CollegeAdmin)

admin.site.register(LastCoupon)

class CouponAdmin(admin.ModelAdmin):
    list_display=('pk','code','sent','sent_to')

admin.site.register(Coupon, CouponAdmin)
