from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from quiz.models import Course, Test, Question
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from typing import *
import logging

logger = logging.getLogger(__name__)


class HomeTeacherPage(UserPassesTestMixin, generic.ListView):
    template_name = 'teacher/teacherpage.html'
    context_object_name = 'courses'

    def test_func(self) -> Optional[bool]:
        return self.request.user.is_teacher

    def get_queryset(self):
        return self.request.user.author_courses.all()

class CourseEditView(UserPassesTestMixin, generic.DetailView):
    model = Course
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({'course_id': self.kwargs['course_id']})
        return context

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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({'course_id': self.kwargs['course_id'],
                        'test_id': self.kwargs['test_id']})
        return context

    def test_func(self) -> Optional[bool]:
        passed = self.request.user == self.get_object(
                            ).authors or self.get_object().authors is None
        logger.info('User %s attempts to access %s Question. Result %s',
                             self.request.user, self.get_object(), passed)
        return passed

    def get_success_url(self) -> str:
        return self.request.path

class CreateQuestionView(UserPassesTestMixin, generic.CreateView):
    model = Question
    template_name = 'teacher/createquestion.html'
    fields = ('photo', 'description',)
    success_url = reverse_lazy('teacherpage')

    def test_func(self) -> Optional[bool]:
        passed = self.request.user in Test.objects.get(
                        pk=self.kwargs['test_id']).authors.all()
        return passed

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({'course_id': self.kwargs['course_id'],
                        'test_id': self.kwargs['test_id']})
        return context

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.authors = self.request.user
        fields.test = Test.objects.get(pk=self.kwargs['test_id'])
        fields.save()
        return super().form_valid(form)

class CreateTestView(UserPassesTestMixin, generic.CreateView):
    model = Test
    template_name = 'teacher/createtest.html'
    fields = ('name', 'description', 'theory',
              'success_percent', 'allotted_time',
              'attempts_number', 'at_start', 'at_finish')
    exclude = ('authors', 'courses',)
    success_url = reverse_lazy('teacherpage')

    def test_func(self) -> Optional[bool]:
        passed = self.request.user in Course.objects.get(
                        pk=self.kwargs['course_id']).teachers.all()
        return passed

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({'course_id': self.kwargs['course_id']})
        return context

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.save()
        fields.courses.add(Course.objects.get(pk=self.kwargs['course_id']))
        fields.authors.add(self.request.user)
        return super().form_valid(form)

class DeleteTestView(generic.DeleteView):
    model = Test
    template_name = 'teacher/deletetest.html' 
    success_url = reverse_lazy('teacherpage')

class DeleteQuestionView(generic.DeleteView):
    model = Question
    template_name = 'teacher/deletequestion.html'
    success_url = reverse_lazy('teacherpage')




