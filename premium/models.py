from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from requests import request

# Create your models here.
class PremiumCourse(models.Model):
    course_title=models.CharField(max_length=30,help_text="Enter The Course Title At Least 10 Words")
    course_slug=models.SlugField(null=False,unique=True)
    course_about=models.CharField(max_length=100,help_text="Enter The Course Details At Least 20 Words")
    what_we_learn=RichTextField()
    course_thumbnail=models.ImageField(upload_to='static/upload/')
    course_join=models.DateTimeField(auto_now_add=True)
    course_price=models.IntegerField()
    course_discount=models.IntegerField(default=0,help_text="Enter The Discount In Percentage Like 25,75 etc.")
    is_active=models.BooleanField(default=False)
    @property
    def discount(self):
        if self.course_discount>0:
            discount_price=self.course_price-self.course_price*self.course_discount/100
        return discount_price

    def get_order(self,user):
        return self.order_set.get(user=user,status="Success")

    def __str__(self):
        return self.course_title
    
    class Meta:
        verbose_name_plural="Course"
    

class PremiumCourseDetail(models.Model):
    course_name=models.ForeignKey(PremiumCourse,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    slug=models.SlugField(null=False,unique=True)
    article=RichTextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Course Detail"
    def __str__(self):
        return self.title

class Paymentstatus:
    SUCCESS="Success"
    PENDING="Pending"
    FAILURE="Failure"

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,editable=False)
    course=models.ForeignKey(PremiumCourse,on_delete=models.DO_NOTHING,editable=False)
    status=models.CharField(default=Paymentstatus.PENDING,max_length=254,blank=False,null=False,editable=False)
    provider_order_id=models.CharField(("Order ID"),max_length=254,null=False,blank=False,editable=False)
    payment_id=models.CharField(max_length=254,null=False,blank=False,editable=False)
    signature_id=models.CharField(max_length=254,null=False,blank=False,editable=False)
    amount=models.IntegerField(editable=False)
    order_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Feedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,editable=False)
    course=models.ForeignKey(PremiumCourse,on_delete=models.DO_NOTHING,editable=False)
    star=models.IntegerField(editable=False)
    say_something=models.TextField(editable=False)
    date=models.DateTimeField(auto_now=True,editable=False)

class Certificate(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(PremiumCourse,on_delete=models.CASCADE)
    upload=models.ImageField(upload_to='static/upload/')