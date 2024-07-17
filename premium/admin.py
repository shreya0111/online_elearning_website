from django.contrib import admin
from premium.models import Certificate, Feedback, Order, PremiumCourse,PremiumCourseDetail

# Register your models here.
# admin.site.register(PremiumCourse)
@admin.register(PremiumCourseDetail)
class PreCourseDetailAdmin(admin.ModelAdmin):
    list_display=('title',)
    prepopulated_fields={"slug":('title',)}
@admin.register(PremiumCourse)
class PremiumCourseAdmin(admin.ModelAdmin):
    list_display=('course_title','is_active',)
    list_editable=['is_active']
    prepopulated_fields={"course_slug":('course_title',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('user','course','status','order_at')
    readonly_fields=['user','course','status','provider_order_id','payment_id','signature_id','amount','order_at']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display=('user','course','star','date',)
    readonly_fields=['user','course','star','say_something','date']

admin.site.register(Certificate)