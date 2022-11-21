from django.db import models
from django.conf import settings
from quiz.models import Answer, Test


class QuestionResault(models.Model):
    right_choices = models.ManyToManyField(Answer, related_name='question_resaults_right', blank=True)
    user_choices = models.ManyToManyField(Answer, related_name='question_resaults_user', blank=True)

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'

class TestResault(models.Model):
    test = models.ForeignKey(Test, related_name='test_results', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_results', on_delete=models.CASCADE)
    question_resaults = models.ManyToManyField(QuestionResault, blank=True)
    is_open = models.BooleanField(verbose_name='Сейчас выполняется')
    passed = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self) -> str:
        return f"{self.test} - {self.user.first_name},{self.user.last_name}"

    class Meta:
        verbose_name = 'Результат Теста'
        verbose_name_plural = 'Результаты Теста'
