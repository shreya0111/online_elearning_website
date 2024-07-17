from django.contrib import admin

from quizapp.models import QuesModel, Result

# Register your models here.
admin.site.register(QuesModel)
admin.site.register(Result)