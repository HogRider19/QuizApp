from django.shortcuts import render
from django.views import View
from django.views import generic
from .models import course, Test
from django.contrib.auth.mixins import UserPassesTestMixin
from .permissions import OnlyAuthenticatedPermission
from typing import *


class HomePage(OnlyAuthenticatedPermission, generic.ListView):
    model = course
    template_name = 'quiz/home.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return self.request.user.get_courses()

class HomeTeacherPage(generic.ListView):
    template_name = 'quiz/teacherpage.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return self.request.user.author_courses.all()

class courseDetailView(OnlyAuthenticatedPermission, generic.DetailView):
    model = course
    template_name = 'quiz/coursedetail.html'
    context_object_name = 'course'

class TestDetailView(OnlyAuthenticatedPermission, generic.DetailView):
    model = Test
    template_name = 'quiz/testdetail.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({'status': context.get('test').get_test_status()})
        return context



