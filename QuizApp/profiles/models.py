from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Group(models.Model):
    """Модель студенческой группы"""
    FACULTY_CHOICES = (
        ('А', 'Ракетно-космической техники'),
        ('Е', 'Оружие и системы вооружения'),
        ('И', 'Информационные и управляющие системы'),
        ('О', 'Естественнонаучный'),
        ('Р', 'Международного менеджмента'),
    )
    STUDY_FORM_CHOICES = (
        ('Б', 'Бакалавриат'),
        ('С', 'Специалитет'),
        ('М', 'Магистратура'),
    )
    faculty = models.CharField(max_length=1, choices=FACULTY_CHOICES, default='А')
    number = models.CharField(max_length=3, default='000', unique=True)
    study_form = models.CharField(max_length=1, choices=STUDY_FORM_CHOICES, default='Б')

    def __str__(self) -> str:
        return f"{self.faculty}{self.number}{self.study_form}"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Profile(models.Model):
    """Модель расширяюшая модель User"""
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_query_name='profiles',
                                blank=True, null=True, on_delete=models.SET_NULL)
    is_teacher = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} - {self.group}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


