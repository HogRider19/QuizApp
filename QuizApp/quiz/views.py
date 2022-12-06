import logging
from typing import *

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import View, generic

from .models import Question, Test, Course
from certification.models import TestResult


logger = logging.getLogger(__name__)


class HomePage(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'quiz/home.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return self.request.user.get_courses()

class CourseDetailView(UserPassesTestMixin, generic.DetailView):
    model = Course
    template_name = 'quiz/coursedetail.html'
    context_object_name = 'course'

    def test_func(self) -> Optional[bool]:
        if not self.request.user.is_authenticated:
            return False
        return self.get_object() in self.request.user.get_courses()

class TestDetailView(UserPassesTestMixin, generic.DetailView):
    model = Test
    template_name = 'quiz/testdetail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        test = context.get('test')
        status = test.get_test_status()
        logger.error(f"GET in quiz : {self.kwargs}")
        available_attempts = test.get_available_attempts(self.request.user)
        context.update({'status': status, 'available_attempts': available_attempts,
                                    'course_id': self.kwargs['course_id']})
        return context

    def test_func(self) -> Optional[bool]:
        if not self.request.user.is_authenticated:
            return False
        return self.get_object() in Test.objects.filter(
                            courses__in=self.request.user.get_courses())


class EstimatesView(LoginRequiredMixin, generic.ListView):
    model = TestResult
    template_name = 'quiz/estimates.html'
    context_object_name = 'test_results_list'

    def get_queryset(self):
        return self.request.user.user_results.all()





