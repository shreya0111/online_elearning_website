from django.contrib import admin

from myapp.models import Course, Course_detail, Video,Contact,Blog

# Register your models here.
# admin.site.register(Course)
class VideoAdmin(admin.TabularInline):
    model=Video
class CourseDetailsAdmin(admin.ModelAdmin):
    list_display=('title',)
    prepopulated_fields={'slug':('title',)}
    inlines=[VideoAdmin,]

admin.site.register(Course_detail,CourseDetailsAdmin)


class CourseInline(admin.TabularInline):
    model = Course_detail

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title',)
    prepopulated_fields={'course_slug':('course_title',)}
# admin.site.register(Course_details)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','contact_id','receiving_time',)
    search_fields=['contact_id']
    list_filter=['contact_id']
    readonly_fields=('name','email','contact_id','subject','receiving_time',)
    list_display_links=['name','email','contact_id']

@admin.register(Blog)
class Blogadmin(admin.ModelAdmin):
    list_display=('blog_title','is_show','created_at')
    list_editable=['is_show']
    search_fields=['title']
    prepopulated_fields={'slug':('blog_title',)}
    list_filter=['created_at']