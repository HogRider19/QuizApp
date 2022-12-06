from django.db import models
from django.conf import settings
from quiz.models import Answer, Test, Question
from django.db.models import F


class QuestionResult(models.Model):
    question = models.ForeignKey(Question, related_name='question_results', on_delete=models.CASCADE)
    right_choices = models.ManyToManyField(Answer, related_name='question_resaults_right', blank=True)
    user_choices = models.ManyToManyField(Answer, related_name='question_resaults_user', blank=True)

    def __str__(self) -> str:
        return self.question.description

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'

class TestResult(models.Model):
    test = models.ForeignKey(Test, related_name='test_results', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_results', on_delete=models.CASCADE)
    question_resaults = models.ManyToManyField(QuestionResult, blank=True)
    is_open = models.BooleanField(verbose_name='Сейчас выполняется')
    passed = models.BooleanField(verbose_name="Пройден", blank=True, null=True, default=False)

    def close(self):
        success_percent = self.test.success_percent
        right_percent = self.get_right_percent()
        allotted_time = self.test.allotted_time

        passed = True if right_percent > success_percent else False

        self.is_open = False
        self.passed = passed
        self.save()

    def get_right_percent(self):
        question_count = self.test.questions.count()
        right_question_count = self.question_resaults.filter(right_choices=F('user_choices')).count()
        return (right_question_count / question_count) * 100

    def __str__(self) -> str:
        return f"{self.test} - {self.user.first_name},{self.user.last_name}"

    class Meta:
        verbose_name = 'Результат Теста'
        verbose_name_plural = 'Результаты Теста'
