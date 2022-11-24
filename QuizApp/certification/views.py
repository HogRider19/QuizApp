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
            return redirect('home')

        manager.open_certification(Test.objects.get(pk=test_pk))
        return redirect('decisioncertification')

    def test_func(self) -> Optional[bool]:
        logger.debug('Request dir: %s', [attr for attr in dir(self.request) if not attr.startswith('__')])
        user_courses = self.request.user.get_courses()
        accessible_test = [user_course.tests for user_course in user_courses]
        return Test.objects.get(pk=self.request.test_pk) in accessible_test


class DecisionView(UserPassesTestMixin, View):
    
    def get(self, request):
        
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


