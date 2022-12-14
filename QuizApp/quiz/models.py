from django.db import models
from profiles.models import Group
from django.db.models import Q
from datetime import datetime
from django.conf import settings


class Course(models.Model):
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

class CourseGroup(models.Model):
    """Промежуточная таблица для модеоей course и Group"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
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
    test = models.ForeignKey('Test', related_name='questions', on_delete=models.CASCADE)
    authors = models.ForeignKey(settings.AUTH_USER_MODEL,
            related_name='compiled_questions', blank=True, null=True, on_delete=models.SET_NULL)

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
    success_percent = models.FloatField(default=50.0)
    allotted_time = models.PositiveIntegerField(default=10)
    attempts_number = models.PositiveIntegerField(default=3)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='compiled_tests', blank=True)
    courses = models.ManyToManyField(Course, related_name='tests')
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

    def get_available_attempts(self, user) -> int:
        user_attempts = user.user_results.filter(test=self, is_open=False).count()
        available_attempts = self.attempts_number - user_attempts
        return available_attempts if available_attempts >= 0 else 0

    def __str__(self) -> str:
        return f"{self.name} - ({self.at_start},{self.at_finish})"

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


