from django.contrib.auth.models import User
from quiz.models import Test, Question, Answer
from functools import wraps
from .models import TestResault, QuestionResault
from typing import List
import logging


logger = logging.getLogger(__name__)


def one_user_one_manger(cls):
    users_managers = {}

    @wraps(cls)
    def iternal(user):

        if user in users_managers:
            return users_managers.get(user)

        obj = cls(user)
        users_managers.update({user: obj})

        return obj 

    return iternal

@one_user_one_manger
class CertificationManager:

    def __init__(self, user: User) -> None:
        self._user = user
        self._test = None
        self._test_resault = None

        self._questions = None
        self._current_question_num = 0

    def is_busy(self):
        open_certification = self._user.user_results.filter(is_open=True)
        if open_certification.count() > 1:
            logger.error('User %s has more that one open test! ', self._user)
        return bool(open_certification)

    def open_certification(self, test: Test):

        if self._test_resault:
            if self._test != self._test_resault.test:
                logger.info("User %s is trying to open more that one test!", self._user)
            return 

        self._test = test
        self._test_resault = TestResault.objects.create(
            test=self._test,
            user=self._user,
            is_open=True,
        )

        self._questions = list(self._test_resault.test.questions.all())

    def close_certification(self):
        ...
        self._test_resault.update(is_open=False)
        self._test_resault.save()
        self._test_resault = None
        self._test = None
        self._questions = None
        self._current_question_num = 0

    def get_next_question(self):
        if self._current_question_num > len(self._questions):
            return None
        
        question = self._questions[self._current_question_num]
        self._current_question_num += 1
        return question

    def get_question(self, question_num: int):
        return self._questions[question_num]

    def set_answer(self, question_num: int, answers: List[Answer]):
        question = self._questions[question_num]
        qr = QuestionResault.objects.create(
            question=question,
        )
        qr.right_choices.appen(qr.question.answers.filter(is_right=True))
        qr.user_choices.append(answers)
        qr.save()

