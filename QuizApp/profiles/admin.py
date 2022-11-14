from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from . import models


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    model = models.Group

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    model = models.User



