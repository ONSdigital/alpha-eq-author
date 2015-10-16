from django.contrib import admin

# Register your models here.
from .models import Survey, Questionnaire

admin.site.register(Survey)
admin.site.register(Questionnaire)
