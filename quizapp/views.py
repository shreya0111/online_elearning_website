from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from quizapp.models import QuesModel,Result
from premium.models import PremiumCourse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="myapp:signin")
def home(request,slug):
    if request.method == 'POST':
        course=get_object_or_404(PremiumCourse,course_slug=slug)
        questions = QuesModel.objects.filter(course=course)
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score/(total*10) * 100
        time=request.POST['timer']
        if(percent>=60):
            result=Result.objects.create(user=request.user,course=course,percentage=percent,score=score,correct=correct,wrong=wrong,time=time,total=total,is_pass=True)
            result.save()
        else:
            result=Result.objects.create(user=request.user,course=course,percentage=percent,score=score,correct=correct,wrong=wrong,time=time,total=total,is_pass=False)
            result.save()
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total,
            'course':course,
        }
        return render(request, 'result.html', context)
    else:
        course=get_object_or_404(PremiumCourse,course_slug=slug)
        questions = QuesModel.objects.filter(course=course)
        context = {
            'questions': questions,
            "course":course
        }
        return render(request, 'quizhome.html', context)