from django.shortcuts import render
from django.views import View
from django.views import generic
from .models import Cource, Test
from django.contrib.auth.mixins import UserPassesTestMixin
from .permissions import OnlyAuthenticatedPermission
from typing import *
import datetime
from django.utils import timezone


class HomePage(OnlyAuthenticatedPermission, generic.ListView):
    model = Cource
    template_name = 'quiz/home.html'
    context_object_name = 'cources'

    def get_queryset(self):
        return self.request.user.profile.group.cources.all()

class CourceDetailView(OnlyAuthenticatedPermission, generic.DetailView):
    model = Cource
    template_name = 'quiz/courcedetail.html'
    context_object_name = 'cource'

class TestDetailView(OnlyAuthenticatedPermission, generic.DetailView):
    model = Test
    template_name = 'quiz/testdetail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        at_start = context.get('test').at_start
        at_finish = context.get('test').at_finish
        time_now = datetime.datetime.now(at_start.tzinfo)
        status = 'open' if at_start < time_now < at_finish else 'close'
        context.update({'status': status})
        return context



