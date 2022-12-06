from django.contrib import admin
from . import models


@admin.register(models.TestResult)
class TestResultAdmin(admin.ModelAdmin):
    model = models.TestResult

@admin.register(models.QuestionResult)
class TestResultAdmin(admin.ModelAdmin):
    model = models.QuestionResult
