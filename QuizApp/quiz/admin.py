from django.contrib import admin
from . import models


class CourceGroupInLine(admin.TabularInline):
    model = models.CourceGroup
    extra = 0

class QuestionAnswerInLine(admin.TabularInline):
    model = models.Answer
    extra = 4

@admin.register(models.Cource)
class CourceAdmin(admin.ModelAdmin):
    model = models.Cource
    inlines = [
        CourceGroupInLine,
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

