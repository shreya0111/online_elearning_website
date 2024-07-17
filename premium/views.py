import json
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from premium.models import Certificate, Feedback, Order, PremiumCourse,Paymentstatus, PremiumCourseDetail
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from quizapp.models import Result
# Create your views here.


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def page_not_found(request):
    return render(request, '404.html')
def home(request):
    premium=PremiumCourse.objects.filter(is_active=True)
    return render(request,"premium.html",{"premium":premium})

@login_required(login_url='myapp:signup')
def premium_course(request,slug):
    # premium=PremiumCourse.objects.get(course_slug=slug)
    premium=get_object_or_404(PremiumCourse,course_slug=slug)
    amount = premium.course_price-premium.course_price*premium.course_discount/100
    amount_paisa=amount*100
    client=razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))
    razorpay_order=client.order.create(dict(amount=int(amount_paisa),currency="INR",payment_capture='1'))
    order=Order.objects.create(user=request.user,course=premium,provider_order_id=razorpay_order["id"],amount=amount)
    order.save()
    is_pay=Order.objects.filter(user=request.user,course=premium,status="Success")
    return render(request,"premiumcourse.html",{"premium":premium,'response':razorpay_order,"is_pay":is_pay})

def course_overview(request,pslug):
    purchase=get_object_or_404(PremiumCourse,course_slug=pslug)
    feedback=Feedback.objects.filter(course=purchase)
    return render(request,'overview.html',{"premium":purchase,"feedback":feedback})



@login_required(login_url="myapp:signup")
def preimum_course_overviews(request, course_slug):
    try:
        premium=PremiumCourse.objects.get(course_slug=course_slug)
    except:
        raise Http404
    try:
        premium_course=PremiumCourseDetail.objects.filter(course_name=premium)
    except PremiumCourseDetail.DoesNotExist:
        raise Http404      
    order=get_object_or_404(Order,user=request.user,course=premium,status="Success")
    return render(request,"premiumoverview.html",{'premium':order,"premium_course":premium_course})

@login_required(login_url="myapp:signup")
def premium_course_detail(request,course_slug,details_slug):
    try:
        premium=PremiumCourse.objects.get(course_slug=course_slug)
    except:
        raise Http404
    try:
        purchase=Order.objects.get(user=request.user,course=premium,status="Success")
    except:
        raise Http404
    
    try:
        premium_course=PremiumCourseDetail.objects.filter(course_name=premium)
    except:
        raise Http404
    cc=get_object_or_404(PremiumCourseDetail,slug=details_slug)
    premium_course_all=get_object_or_404(PremiumCourseDetail,slug=details_slug,course_name=premium)
    try:
        next_page = premium_course_all.get_next_by_created()
    except:
        next_page = None
    try:
        prev_page = premium_course_all.get_previous_by_created()
    except:
        prev_page = None
    f=Feedback.objects.filter(user=request.user,course=premium).exists()
    exam=Result.objects.filter(user=request.user,course=premium).exists()
    # exm=get_object_or_404(Result,user=request.user,course=premium)
    try:
        exm=Result.objects.filter(user=request.user,course=premium).first()
    except:
        print('error')
    if request.method=="POST":
        ratings=request.POST['rating']
        say_something=request.POST['say_something']
        feedback=Feedback.objects.create(course=premium,user=request.user,star=ratings,say_something=say_something)
        feedback.save()
        messages.success(request,"Thank you for your valueable feedback")
        return redirect('myapp:home')
    return render(request,"premiumcoursedetails.html",{"purchase":purchase,"premium_course":premium_course,"premium_course_all":premium_course_all,"cc":cc,"premium":premium,"next_page":next_page,"prev_page":prev_page,"f":f,"exam":exam,"exm":exm})

def form_success(request):
    return render('success.html')