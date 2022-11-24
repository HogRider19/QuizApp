from django.shortcuts import render, redirect
from django.views import View
from .certificationManager import CertificationManager
from django.contrib.auth.mixins import UserPassesTestMixin
from typing import Optional
from quiz.models import course, Test
import logging


logger = logging.getLogger(__name__)


class StartCertificationView(UserPassesTestMixin, View):

    def post(self, request, test_pk):
        
        manager = CertificationManager(request.user)

        if manager.is_busy():
            manager.close_certification()

        manager.open_certification(Test.objects.get(pk=test_pk))
        return redirect('decisioncertification', 0)

    def test_func(self) -> Optional[bool]:
        user_courses = self.request.user.get_courses()
        accessible_test = sum([list(user_course.tests.all()) for user_course in user_courses], [])
        return Test.objects.get(pk=self.kwargs.get('test_pk')) in accessible_test


class DecisionView(UserPassesTestMixin, View):
    
    def get(self, request, question_num):
        
        manager = CertificationManager(request.user)
        question = manager.get_next_question()

        if question:
            return render(request, 'certification/decisionquestion.html', {'question': question})

        return redirect('finishcertification')

    def post(self, request):
        pass

    def test_func(self) -> Optional[bool]:
        return not self.request.user.is_anonymous


class FinishCertificationView(UserPassesTestMixin, View):

    def post(self, request):
        
        manager = CertificationManager(request.user)
        manager.close_certification()

        return redirect('home')

    def test_func(self) -> Optional[bool]:
        return not self.request.user.is_anonymous


