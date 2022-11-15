from django.contrib import admin
from . import models


class courseGroupInLine(admin.TabularInline):
    model = models.courseGroup
    extra = 0

class QuestionAnswerInLine(admin.TabularInline):
    model = models.Answer
    extra = 4

@admin.register(models.course)
class courseAdmin(admin.ModelAdmin):
    model = models.course
    inlines = [
        courseGroupInLine,
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

