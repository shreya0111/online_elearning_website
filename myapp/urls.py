from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
app_name='myapp'
urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.register,name='signup'),
    path('signin/',views.user_login,name='signin'),
    path('logout/',views.user_logout,name="logout"),
    path('course/<slug:slug>/',views.course,name="cours"),
    path('course/<slug:sslug>/<slug:slugpost>/',views.course_details,name="course_details"),
    path('search/',views.search,name="search"),
    path('course/',views.allcourse,name="allcourse"),
    path('contact/',views.contact,name="contact"),
    path('blog/',views.blogapp,name="blogapp"),
    path('blog/<slug:slug>',views.blogs_detail,name="blogs_detail"),
    path('dashboard/',views.dashboard,name="dboard"),
    path('success/', views.callback, name="success"),
    path('dashboard/notification/',views.dashboard_notification,name="notify"),
    path('dashboard/purchased/', views.dashboard_purchased_course,name="purchased"),
    path('change-password/',views.password_change,name="password")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)