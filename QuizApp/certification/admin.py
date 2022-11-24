from django.contrib import admin
from . import models


@admin.register(models.TestResault)
class TestResaultAdmin(admin.ModelAdmin):
    model = models.TestResault

@admin.register(models.QuestionResault)
class TestResaultAdmin(admin.ModelAdmin):
    model = models.QuestionResault
