from django.db import models
from profiles.models import Group
from django.db.models import Q
from datetime import datetime
from django.conf import settings


class course(models.Model):
    """Модель обучающего курса"""
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=5000, blank=True, null=True, verbose_name='Описание')
    groups = models.ManyToManyField(Group, related_name='courses', through='courseGroup')
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='author_courses', blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class courseGroup(models.Model):
    """Промежуточная таблица для модеоей course и Group"""
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    time_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.course} - {self.group}"
    
    class Meta:
        verbose_name = 'Курс-Группа'
        verbose_name_plural = 'Курсы-Группы'

class Question(models.Model):
    """Модель вопроса из теста"""
    photo = models.ImageField(upload_to='questionImages', blank=True, null=True)
    description = models.TextField(max_length=5000)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='compiled_questions', blank=True)

    def __str__(self) -> str:
        return f"{self.description[:60]}..." if len(self.description
                                                ) > 60 else f"{self.description}"

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    """Модель ответов к вопросу"""
    description = models.TextField(max_length=1000)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    is_right = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.description[:60]}..." if len(self.description
                                        ) > 60 else f"{self.description}"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Test(models.Model):
    """Модель теста в курсе"""
    name = models.CharField(max_length=100, default='Высшая сатематика')
    description = models.TextField(max_length=5000, blank=True, null=True)
    theory = models.TextField(blank=True, null=True)
    questions = models.ManyToManyField(Question, related_name='test')
    success_percent = models.FloatField(default=50.0)
    allotted_time = models.PositiveIntegerField(default=10)
    attempts_number = models.PositiveIntegerField(default=3)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='compiled_tests', blank=True)
    courses = models.ManyToManyField(course, related_name='tests')
    at_start = models.DateTimeField(blank=True, null=True)
    at_finish = models.DateTimeField(blank=True, null=True)

    def get_test_status(self) -> str:
        time_now = datetime.now(self.at_start.tzinfo)

        status = None
        if self.at_start < time_now < self.at_finish:
            status = 'open'
        elif time_now < self.at_start:
            status = 'wait'
        else:
            status = 'close'

        return status

    def __str__(self) -> str:
        return f"{self.name} - ({self.at_start},{self.at_finish})"

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

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
    passed = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self) -> str:
        return f"{self.test} - {self.user.first_name},{self.user.last_name}"

    class Meta:
        verbose_name = 'Результат Теста'
        verbose_name_plural = 'Результаты Теста'
