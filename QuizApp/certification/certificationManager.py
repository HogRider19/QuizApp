from django.contrib.auth.models import User
from quiz.models import Test, Question, Answer
from functools import wraps
from .models import TestResult, QuestionResult
from typing import List
import logging
from django.http import Http404


logger = logging.getLogger(__name__)


class one_user_one_manger:

    users_managers = {}

    def __call__(self, cls):

        @wraps(cls)
        def iternal(user):

            manager = None
            if user in self.users_managers:
                logger.debug("Received already created manager for %s", user)
                manager = self.users_managers.get(user)
            else:
                manager = cls(user)
                self.users_managers.update({user: manager})
                logger.debug("Created a new manager for %s", user)

            manager._update_attrs_using_db()
            manager._decorator = self
            return manager

        return iternal

    def delete_manager(self, user: User):
        del self.users_managers[user]
        logger.warning("delete_manager, user: %s", user)


@one_user_one_manger()
class CertificationManager:

    def __init__(self, user: User) -> None:
        self._user = user
        self._test = None
        self._test_result = None

        self._questions = None
        self._current_question_num = 0

    def is_busy(self):
        open_certification = self._user.user_results.filter(is_open=True)
        if open_certification.count() > 1:
            logger.error('User %s has more that one open test! ', self._user)
        logger.debug("User %s, Check is_busy: %s",
                     self._user, bool(open_certification))
        logger.debug("User %s,  open_certification: %s",
                     self._user, open_certification)
        return bool(open_certification)

    def open_certification(self, test: Test):

        self._update_attrs_using_db()

        if self.is_busy():
            logger.debug(
                "User %s is trying to open a non-closed certification", self._user)
            if self._test != self._test_result.test:
                logger.info(
                    "User %s is trying to open more that one test!", self._user)
            return

        logger.debug("User %s openes the certification", self._user)

        self._test = test
        self._test_result = TestResult.objects.create(
            test=self._test,
            user=self._user,
            is_open=True,
        )

        self._questions = list(self._test_result.test.questions.all())

        logger.debug("User %s, questions: %s", self._user, self._questions)

    def close_certification(self):
        ...

        if not self.is_busy():
            return

        logger.debug("User %s closes the certification", self._user)

        self._update_attrs_using_db()

        self._test_result.close()
        self._test_result = None
        self._test = None
        self._questions = None
        self._current_question_num = 0
        self._decorator.delete_manager(self._user)

    def shift_question_pointer(self):
        self._current_question_num += 1

    def get_question(self, question_num: int):
        logger.debug(
            "User %s receives the question(get_question), num: %s", self._user, question_num)
        if not 0 <= question_num < len(self._questions):
            if question_num == len(self._questions):
                logger.debug(
                    "User %s receives the last question(get_question), num: %s", self._user, question_num)
                return None
            logger.debug(
                "User %s, (get_question) question_num out of range, num: %s", self._user, question_num)
            raise Http404
        return self._questions[question_num]

    def set_answer(self, question_num: int, post: dict):
        answers = self._get_answers_from_post(post)
        question = self._questions[question_num]

        self._test_result.question_resaults.filter(
            question__id=question.id).delete()

        qr = QuestionResult.objects.create(
            question=question,
        )
        qr.right_choices.set(question.answers.filter(is_right=True))
        qr.user_choices.set(answers)
        qr.save()

        self._test_result.question_resaults.add(qr)

    def get_test_result(self):
        return self._test_result

    @property
    def last_question_num(self):
        return len(self._questions) - 1

    def _update_attrs_using_db(self):
        """???????????????????? ???????????? ???? ???? ?? ????????????"""
        logger.debug("User %s, Update attrs", self._user)
        if self.is_busy():
            self._test_result = self._user.user_results.get(is_open=True)
            self._questions = list(self._test_result.test.questions.all())
        self._current_question_num = 0

    def _get_answers_from_post(self, post: dict):
        answers_id = [int(value) for name, value in post.items()
                      if name.startswith('answer_id')]
        answers = Answer.objects.filter(id__in=answers_id)
        return answers
