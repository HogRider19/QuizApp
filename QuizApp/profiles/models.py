from django.db import models
from django.contrib.auth.models import AbstractUser


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


class User(AbstractUser):
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    group = models.ForeignKey(Group, related_name='profiles',
                            blank=True, null=True, on_delete=models.SET_NULL, default=None)
    is_teacher = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {'Учитель' if self.is_teacher else self.group}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['email'], name="unique_email_profile"
            )
        ]

