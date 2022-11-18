from django.shortcuts import render
from django.views import View
from django.views import generic
from quiz.models import course, Test, Question
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from typing import *

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
        return self.request.user.is_teacher

class TestEditView(UserPassesTestMixin, generic.DetailView):
    model = Test
    template_name = 'teacher/testedit.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        questions = context.get('test').questions.all()
        context.update({'questions': questions})
        return context

    def test_func(self) -> Optional[bool]:
        return self.request.user.is_teacher

class QuestionEditView(UserPassesTestMixin, generic.UpdateView):
    model = Question
    template_name = 'teacher/questionedit.html'
    context_object_name = 'question'
    fields = ('photo', 'description')

    def test_func(self) -> Optional[bool]:
        return self.request.user.is_teacher