from django.shortcuts import render
from django.views import View
from django.views import generic
from .models import course, Test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .permissions import OnlyAuthenticatedPermission
from typing import *


class HomePage(LoginRequiredMixin, generic.ListView):
    model = course
    template_name = 'quiz/home.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return self.request.user.get_courses()

class courseDetailView(LoginRequiredMixin, generic.DetailView):
    model = course
    template_name = 'quiz/coursedetail.html'
    context_object_name = 'course'

class TestDetailView(LoginRequiredMixin, generic.DetailView):
    model = Test
    template_name = 'quiz/testdetail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({'status': context.get('test').get_test_status()})
        return context

class HomeTeacherPage(generic.ListView):
    template_name = 'quiz/teacherpage.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return self.request.user.author_courses.all()

class CourseEditView(UserPassesTestMixin, generic.DetailView):
    model = course
    template_name = 'quiz/courseedit.html'
    context_object_name = 'course'

    def test_func(self) -> Optional[bool]:
        return self.request.user.is_teacher

class TestEditView(UserPassesTestMixin, generic.DetailView):
    model = Test
    template_name = 'quiz/testedit.html'
    context_object_name = 'test'

    def test_func(self) -> Optional[bool]:
        return self.request.user.is_teacher





