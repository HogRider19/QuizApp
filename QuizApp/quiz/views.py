import logging
from typing import *

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import View, generic

from .models import Question, Test, course
from .permissions import OnlyAuthenticatedPermission


logger = logging.getLogger(__name__)


class HomePage(LoginRequiredMixin, generic.ListView):
    model = course
    template_name = 'quiz/home.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return self.request.user.get_courses()

class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = course
    template_name = 'quiz/coursedetail.html'
    context_object_name = 'course'

class TestDetailView(LoginRequiredMixin, generic.DetailView):
    model = Test
    template_name = 'quiz/testdetail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        status = context.get('test').get_test_status()
        logger.debug("Status test: %s", status)
        context.update({'status': status})
        return context






