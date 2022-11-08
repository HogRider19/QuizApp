from django.contrib import admin
from . import models


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    model = models.Group

@admin.register(models.Profile)
class GroupAdmin(admin.ModelAdmin):
    model = models.Profile


