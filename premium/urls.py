from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from premium import views
app_name="premium"
urlpatterns = [
    path('',views.home,name="home"),
    path('overview/<slug:pslug>/',views.course_overview,name="overview"),
    path('overview/<slug:slug>/payment/',views.premium_course,name='premium_course'),
    # path('callback/',views.pay_sucess,name='success'),
    path('premium/<slug:course_slug>',views.preimum_course_overviews,name="premium_course_overview"),
    path('premium/<slug:course_slug>/<slug:details_slug>/',
         views.premium_course_detail, name="premium_course_details"),
    path('form-success/',views.form_success),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)