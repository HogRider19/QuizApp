import logging
from typing import Optional

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views import View
from quiz.models import Test

from .certificationManager import CertificationManager
from .models import TestResult


logger = logging.getLogger(__name__)


class StartCertificationView(UserPassesTestMixin, View):
    def post(self, request, test_pk):

        manager = CertificationManager(request.user)

        manager.open_certification(Test.objects.get(pk=test_pk))

        return redirect('decisioncertification', 0)

    def test_func(self) -> Optional[bool]:
        user_courses = self.request.user.get_courses()
        accessible_test = sum([list(user_course.tests.all())
                              for user_course in user_courses], [])
        test = Test.objects.get(pk=self.kwargs.get('test_pk'))
        available_attempts = test.get_available_attempts(self.request.user)
        return test in accessible_test and available_attempts > 0


class DecisionView(UserPassesTestMixin, View):

    def get(self, request, question_num):

        manager = CertificationManager(request.user)
        question = manager.get_question(question_num)

        if question:
            return render(request, 'certification/decisionquestion.html',
                          {'question': question, 'question_num':  question_num,
                           'last_question_num': manager.last_question_num})

        return redirect('finishpage')

    def post(self, request, question_num):

        manager = CertificationManager(request.user)

        manager.set_answer(question_num, request.POST)

        return redirect('decisioncertification', question_num+1)

    def test_func(self) -> Optional[bool]:
        return not self.request.user.is_anonymous


class FinishCertificationView(UserPassesTestMixin, View):

    def post(self, request):

        manager = CertificationManager(request.user)
        test_result = manager.get_test_result()
        manager.close_certification()

        return redirect('testresultpage', test_result.id)

    def test_func(self) -> Optional[bool]:
        return not self.request.user.is_anonymous


class FinishPageView(View):

    def get(self, requeset):
        return render(requeset, 'certification/finishpage.html', {})


class TestResultPageView(View):

    def get(self, request, tr_pk):
        test_result = TestResult.objects.get(id=tr_pk)
        return render(request, 'certification/testresultpage.html', {'test_result': test_result})
