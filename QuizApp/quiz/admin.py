from django.contrib import admin
from .models import Cource, CourceGroup
from profiles.models import Profile, Group


class CourceGroupAdmin(admin.TabularInline):
    model = CourceGroup
    extra = 0

@admin.register(Cource)
class CourceAdmin(admin.ModelAdmin):
    model = Cource
    inlines = [
        CourceGroupAdmin,
    ]

