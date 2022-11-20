from django.shortcuts import render
from django.views import View
from django.views import generic
from quiz.models import course, Test, Question
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from typing import *
import logging

logger = logging.getLogger(__name__)


class HomeTeacherPage(generic.ListView):
    template_name = 'teacher/teacherpage.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return self.request.user.author_courses.all()

class CourseEditView(UserPassesTestMixin, generic.DetailView):
    model = course
    template_name = 'teacher/courseedit.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tests = context.get('course').tests.all()
        context.update({'tests': tests})
        return context

    def test_func(self) -> Optional[bool]:
        is_pass = self.request.user in self.get_object().teachers.all()
        logger.info('User %s attempts to access %s course. Result %s',
                             self.request.user, self.get_object(), is_pass)
        return is_pass

class TestEditView(UserPassesTestMixin, generic.UpdateView):
    model = Test
    template_name = 'teacher/testedit.html'
    context_object_name = 'test'
    fields = ('name', 'description', 'at_start', 'at_finish')

    def test_func(self) -> Optional[bool]:
        is_pass = self.request.user in self.get_object().authors.all()
        logger.info('User %s attempts to access %s test. Result %s',
                             self.request.user, self.get_object(), is_pass)
        return is_pass

    def get_success_url(self) -> str:
        return self.request.path

    def form_valid(self, form):
        return super().form_valid(form)

class QuestionEditView(UserPassesTestMixin, generic.UpdateView):
    model = Question
    template_name = 'teacher/questionedit.html'
    context_object_name = 'question'
    fields = ('photo', 'description')

    def test_func(self) -> Optional[bool]:
        is_pass = self.request.user in self.get_object().authors.all()
        logger.info('User %s attempts to access %s Question. Result %s',
                             self.request.user, self.get_object(), is_pass)
        return is_pass

    def get_success_url(self) -> str:
        return self.request.path
