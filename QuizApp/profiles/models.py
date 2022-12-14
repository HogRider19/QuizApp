from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


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
        ('П', 'Повыгение квалификации'),
    )
    YEAR_ADMISSION_CHOICES = [(str(r), str(r)) for r in range(1980, (datetime.datetime.now().year+1))]
    DEPARTMENT_CHOICES = [(str(r), str(r)) for r in range(1, 10)]
    NUMBER_CHOICES = [(str(r), str(r)) for r in range(1, 9)]

    faculty = models.CharField(max_length=1, choices=FACULTY_CHOICES, default='А')
    department = models.CharField(max_length=1, choices=DEPARTMENT_CHOICES, default='0')
    number = models.CharField(max_length=1, choices=NUMBER_CHOICES, default='0')
    year_admission = models.CharField(max_length=4, choices=YEAR_ADMISSION_CHOICES,
                                     default='2000', verbose_name='Год посткпления')
    study_form = models.CharField(max_length=1, choices=STUDY_FORM_CHOICES, default='Б')

    def __str__(self) -> str:
        return f"{self.faculty}{self.department}{self.year_admission[-1]}{self.number}{self.study_form}"

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'


class User(AbstractUser):
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    group = models.ForeignKey(Group, related_name='users', verbose_name='Учебная группа',
                            blank=True, null=True, on_delete=models.SET_NULL, default=None)
    is_teacher = models.BooleanField(default=False, verbose_name='Является учителем')

    def get_courses(self):
        if self.group:
            return self.group.courses.all()
        return []

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {'Учитель' if self.is_teacher else f'Ученик {self.group}'}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['email'], name="unique_email_profile"
            )
        ]

