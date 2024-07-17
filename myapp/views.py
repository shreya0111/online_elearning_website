from email import message
import json
from traceback import walk_tb
from django.http import BadHeaderError, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from myapp.models import Blog, Contact, Course, Course_detail,Video
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import datetime
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from premium.models import PremiumCourse, PremiumCourseDetail
from django.views.decorators.csrf import csrf_exempt
import razorpay
from premium.models import Order,Paymentstatus
from numerize import numerize
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Create your views here.
def home(request):
    course=Course.objects.filter(is_active=True).order_by('-course_join')[0:3]
    allblog = Blog.objects.filter(is_show=True).order_by('-created_at')[0:2]
    premium=PremiumCourse.objects.filter(is_active=True).order_by('-course_join')[0:3]
    course1=Course.objects.filter(is_active=True).count()
    course2=PremiumCourse.objects.filter(is_active=True).count()
    total_count=numerize.numerize(course1+course2)
    course_count=numerize.numerize(course1)
    premium_count=numerize.numerize(course2)
    user=User.objects.filter(is_active=True).count()
    user_count=numerize.numerize(user)
    context={'course':course,"allblog":allblog,"premium":premium,"total_count":total_count,"course_count":course_count,"premium_count":premium_count,"user_count":user_count}
    return render(request,'index.html',context)

def course(request,slug):
    slugpost = get_object_or_404(Course, course_slug=slug)
    course=Course_detail.objects.filter(course_name=slugpost)
    return render(request,'course.html',{"slugpost":slugpost,"course":course})

def course_details(request,sslug,slugpost):
    slugpos = get_object_or_404(Course, course_slug=sslug)
    course=Course_detail.objects.filter(course_name=slugpos)
    cc=Course_detail.objects.get(slug=slugpost)
    # ccc=Course_detail.objects.filter(course_name=course_name)
    video=Video.objects.get(course=cc,is_active=True)
    c1=Course_detail.objects.get(course_name=slugpos,slug=slugpost)
    # c2=Course_detail.objects.get(course_name=slugpos,slug=slugpost).next()
    # print(c2)
    print(c1)
    try:
        next_page=c1.get_next_by_created()
    except:
        next_page=None
    try:
        prev_page = c1.get_previous_by_created()
    except:
        prev_page = None
    return render(request,'course_detail.html',{"slugpos":slugpos,"course":course,"cc":cc,"video":video,"next_page":next_page,"prev_page":prev_page})
def register(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        username=request.POST['user']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if fname=="" and lname=="" and email=="" and username=="" and pass1=="" and pass2=="":
            messages.warning(request,"You must fill all the form")
            return redirect('myapp:signup')
        if len(fname)<2 and len(lname)<2:
            messages.warning(request,"First name and Last Name Must Greater Than 2")
        if email!=username:
            messages.warning(request,"Email and Confirm Email not mathcing")
            return redirect('myapp:signup')
        if not pass1.isalnum():
            messages.warning(request,"Password should alphanumeric")
            return redirect('myapp:signup')
        if len(pass1)<8:
            messages.warning(request,"Password Must Be Greater Than 8")
            return redirect('myapp:signup')
            
        if pass1!=pass2:
            messages.warning(request,'Please confirm the password')
            return redirect('myapp:signup')

        matchmail=User.objects.filter(email=email).first()
        matchUserName = User.objects.filter(username=username).first()
        if matchmail:
            messages.warning(request,'This mail already register')
            return redirect('myapp:signin')

        if matchUserName:
            messages.warning(request, "This user already taken by someone")
            return redirect('myapp:signup')
        user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=pass1)
        user.save()
        messages.success(request,"You are successfully created your account")
        return redirect('myapp:signin')
    return render(request,'signup.html')

def user_login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        if email=="" and password=="":
            messages.warning(request,"You must fill all the form")
            return redirect("myapp:signin")
        matchEmail=User.objects.filter(username=email).first()
        matchPassword=User.objects.filter(password=password).first()
        if not matchEmail:
            messages.warning(request,"This email is not register please register this mail.")
            return redirect('myapp:signup')
        # if not matchPassword:
        #     messages.warning(request,"Wrong Password")
        #     return redirect('myapp:signin')
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are successfully login")
            return redirect('myapp:home')
        else:
            return redirect('myapp:signup')
    return render(request,"signin.html")

@login_required(login_url='myapp:signup')
def user_logout(request):
    logout(request)
    messages.success(request,"You are successfully logout")
    return redirect('myapp:home')


# search-------------------------
def search(request):
    query=request.GET.get('q','')
    searchFilter=Course.objects.filter(Q(course_title__icontains=query)|Q(what_we_learn__icontains=query)).distinct()
    search_premium=PremiumCourse.objects.filter(Q(course_title__icontains=query)|Q(what_we_learn__icontains=query)).distinct()
    return render(request,'search.html',{'searchfilter':searchFilter,'query':query,'search_premium':search_premium})

# allcourse--------------
def allcourse(request):
    course=Course.objects.filter(is_active=True)
    return render(request,'allcourse.html',{"course":course})

#contact-----------------
def contact(request):
    rand='IJMPSST'+''.join([random.choice(string.digits) for n in range(16)])
    time=datetime.datetime.now()
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        if name=="" and email=="" and message=="":
            messages.warning(request,"You must fill all the forms")
            return redirect('myapp:contact')
        if email=="":
            messages.warning(request,"Your email should not blank")
            return redirect('myapp:contact')
        if len(name)<5:
            messages.warning(request,"Your name must greater than 5")
            return redirect('myapp:contact')
        if len(message)<10:
            messages.warning(request,"Message should greater than 10")
            return redirect('myapp:contact')
        email_from=settings.EMAIL_HOST_USER
        subject=name+" , You send us a mail. Please wait for our reply. Your Mail is:' "+message+" 'and your Contact ID is: "+rand
        if name and email and message:
            try:
                send_mail(name,subject,email_from,[email])
            except BadHeaderError:
                return HttpResponse("Invalid bad head error")
        messages.success(request,"Your message successfully sent. Please wait for reply")
        contact=Contact.objects.create(name=name,email=email,subject=message,contact_id=rand,receiving_time=time)
        contact.save()
        return redirect('myapp:home')
    return render(request,'contact.html')



#blog-----------------------------

def blogapp(request):
    b=Blog.objects.filter(is_show=True)
    return render(request,'blog.html',{"b":b})

def blogs_detail(request,slug):
    b=get_object_or_404(Blog,slug=slug)
    course=Course.objects.all().order_by('-course_join')[0:3]
    allblog=Blog.objects.all().order_by('-created_at')[0:3]
    return render(request,'blog_details.html',{'b':b,"course":course,"allblog":allblog})

@login_required(login_url='myapp:signup')
def dashboard(request):
    purchased=Order.objects.filter(user=request.user,status="Success").order_by('-order_at')[0:3]
    return render(request,'dashbord.html',{"purchase":purchased})

@login_required(login_url="myapp:signup")
def dashboard_notification(request):
    success=Order.objects.filter(user=request.user,status="Success")
    fail=Order.objects.filter(user=request.user,status="Failure")
    return render(request,'notification.html',{"success":success,"fail":fail})

@login_required(login_url="myapp:signup")
def dashboard_purchased_course(request):
    try:
        premium=Order.objects.filter(user=request.user,status="Success")
    except Order.DoesNotExist:
        raise Http404
    return render(request,"purchase_course.html",{'premium':premium})

@csrf_exempt
def callback(request):
    if request.method=="POST":
        try:
            data=request.POST
            client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
            verify=client.utility.verify_payment_signature(data)
            payment_id = request.POST.get("razorpay_payment_id", "")
            provider_order_id = request.POST.get("razorpay_order_id", "")
            signature_id = request.POST.get("razorpay_signature", "")
            order=Order.objects.get(provider_order_id=provider_order_id)
            order.payment_id=payment_id
            order.signature_id=signature_id
            order.save()
            if verify:
                order.status=Paymentstatus.SUCCESS
                order.save()
                return render(request,'success_page.html',{'status':order.status})
            else:
                order.status=Paymentstatus.FAILURE
                order.save()
                return render(request,'sucess_page.html',{'status':order.status})
            return render(request,'success_page.html')
        except:
            payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
            provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
             "order_id"
            )
            order = Order.objects.get(provider_order_id=provider_order_id)
            order.payment_id = payment_id
            order.status = Paymentstatus.FAILURE
            order.save()
            return render(request,'success_page.html',{"status":order.status})
    return render(request,'success_page.html')

def password_change(request):
    if request.method=="POST":
        form=PasswordChangeForm(user=request.user,data=request.POST)
        print("pass1")
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('myapp:home')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,"changepass.html",{"form":form})