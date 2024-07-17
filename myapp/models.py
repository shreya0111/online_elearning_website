from distutils.command.upload import upload
from django.db import models
from ckeditor.fields import RichTextField
from numpy import require

# Create your models here.

class Course(models.Model):
    course_title=models.CharField(max_length=30,help_text="Enter The Course Title At Least 10 Words")
    course_slug=models.SlugField(null=False,unique=True)
    course_about=models.CharField(max_length=100,help_text="Enter The Course Details At Least 20 Words")
    what_we_learn=RichTextField()
    course_thumbnail=models.ImageField(upload_to='static/upload/')
    course_join=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.course_title

class Course_detail(models.Model):
    course_name=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    slug=models.SlugField(null=False,unique=True)
    article=RichTextField()
    created=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Course Detail"

class Video(models.Model):
    title=models.CharField(max_length=100,null=False)
    course=models.ForeignKey(Course_detail,on_delete=models.CASCADE)
    video_id=models.CharField(max_length=100,null=False)
    is_active=models.BooleanField(default=False)

class Contact(models.Model):
    name=models.CharField(max_length=50,editable=False)
    email=models.EmailField(max_length=250,editable=False)
    subject=models.TextField(editable=False)
    contact_id=models.CharField(max_length=50,editable=False,unique=True)
    receiving_time=models.CharField(max_length=85,editable=False)


class Blog(models.Model):
    blog_title = models.CharField(max_length=255)
    slug = models.SlugField()
    blog_about=models.CharField(max_length=100,help_text="Enter The Course Details At Least 20 Words")
    blog_content = RichTextField()
    thumbnail = models.ImageField(upload_to='static/upload/')
    is_show = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
