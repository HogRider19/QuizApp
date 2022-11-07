from django.db import models
from profiles.models import Group, Profile


class Cource(models.Model):
    """Модель обучающего курса"""
    name = models.CharField(max_length=250)
    groups = models.ManyToManyField(Group, related_name='cources', through='CourceGroup')
    teachers = models.ManyToManyField(Profile, related_name='author_courses', blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class CourceGroup(models.Model):
    """Промежуточная таблица для модеоей Cource и Group"""
    cource = models.ForeignKey(Cource, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    time_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.cource} - {self.group}"
    
    class Meta:
        verbose_name = 'Курс-Группа'
        verbose_name_plural = 'Курсы-Группы'

class Question(models.Model):
    """Модель вопроса из теста"""
    photo = models.ImageField(upload_to='questionImages', blank=True, null=True)
    description = models.TextField(max_length=5000)
    authors = models.ManyToManyField(Profile, related_name='compiled_questions')

    def __str__(self) -> str:
        return super().__str__()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    """Модель ответов к вопросу"""
    description = models.TextField(max_length=1000)
    question = models.ForeignKey(Profile, related_name='answers', on_delete=models.CASCADE)
    is_right = models.BooleanField(default=True)

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
    authors = models.ManyToManyField(Question, related_name='compiled_tests')
    at_start = models.DateTimeField(blank=True, null=True)
    at_finish = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} - ({self.at_start},{self.at_finish})"

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
