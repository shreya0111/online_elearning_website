from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from quizapp import views
app_name="quizapp"
urlpatterns = [
    path("<slug:slug>/",views.home,name="quizhome"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)