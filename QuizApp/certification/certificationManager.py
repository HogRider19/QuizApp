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
            logger.debug("Received already created manager for %s", user)
            return users_managers.get(user)

        obj = cls(user)
        users_managers.update({user: obj})

        logger.debug("Created a new manager for %s", user)

        logger.debug("Users_managers: %s", users_managers)

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
        logger.debug("User %s, Check is_busy: %s", self._user, bool(open_certification))
        logger.debug("User %s,  open_certification: %s", self._user, open_certification)
        return bool(open_certification)

    def open_certification(self, test: Test):

        if self._test_resault:
            logger.debug("User %s is trying to open a non-closed certification", self._user)
            if self._test != self._test_resault.test:
                logger.info("User %s is trying to open more that one test!", self._user)
            return
        
        logger.debug("User %s openes the certification", self._user)

        self._test = test
        self._test_resault = TestResault.objects.create(
            test=self._test,
            user=self._user,
            is_open=True,
        )

        self._questions = list(self._test_resault.test.questions.all())

        logger.debug("User %s, questions: %s", self._user, self._questions)

    def close_certification(self):
        ...
        if not self.is_busy():
            return

        logger.debug("User %s closes the certification", self._user)

        self._test_resault.is_open = False
        self._test_resault.save()
        self._test_resault = None
        self._test = None
        self._questions = None
        self._current_question_num = 0

    def get_next_question(self):
        if self._current_question_num > len(self._questions):
            logger.debug("User %s is tryng to receives last question, num: %s", self._user, self._current_question_num)
            return None

        logger.debug("User %s receives the question, num: %s", self._user, self._current_question_num)
        
        question = self._questions[self._current_question_num]
        logger.debug("User %s, current question: %s", self._user, question)
        self._current_question_num += 1
        return question

    def get_question(self, question_num: int):
        logger.debug("User %s receives the question(get_question), num: %s", self._user, question_num)
        return self._questions[question_num]

    def set_answer(self, question_num: int, answers: List[Answer]):
        logger.debug("User %s (set_answer), question_num: %s, answers:  %s", self._user, question_num, answers)
        question = self._questions[question_num]
        qr = QuestionResault.objects.create(
            question=question,
        )
        qr.right_choices.appen(qr.question.answers.filter(is_right=True))
        qr.user_choices.append(answers)
        qr.save()

