from django.db import models
from premium.models import PremiumCourse
from django.contrib.auth.models import User
# Create your models here.


class QuesModel(models.Model):
    course=models.ForeignKey(PremiumCourse,on_delete=models.CASCADE)
    question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.question

class Result(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(PremiumCourse,on_delete=models.CASCADE)
    percentage=models.IntegerField()
    score=models.IntegerField()
    correct=models.IntegerField()
    wrong=models.IntegerField()
    time=models.IntegerField()
    total=models.IntegerField()
    is_pass=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name}+{self.score}+{self.percentage}"

