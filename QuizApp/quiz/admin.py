from django.contrib import admin
from . import models


class CourseGroupInLine(admin.TabularInline):
    model = models.CourseGroup
    extra = 0

class QuestionAnswerInLine(admin.TabularInline):
    model = models.Answer
    extra = 4

@admin.register(models.Course)
class courseAdmin(admin.ModelAdmin):
    model = models.Course
    inlines = [
        CourseGroupInLine,
    ]

@admin.register(models.Answer)
class GroupAdmin(admin.ModelAdmin):
    model = models.Answer

@admin.register(models.Question)
class GroupAdmin(admin.ModelAdmin):
    model = models.Question
    inlines = [
        QuestionAnswerInLine,
    ]

@admin.register(models.Test)
class GroupAdmin(admin.ModelAdmin):
    model = models.Test

