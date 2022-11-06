from django.db import models
from profiles.models import Group, Profile


class Cource(models.Model):
    name = models.CharField(max_length=250)
    groups = models.ManyToManyField(Group, related_query_name='cources', through='CourceGroup')
    teachers = models.ManyToManyField(Profile, related_query_name='author_courses', blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class CourceGroup(models.Model):
    cource = models.ForeignKey(Cource, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    time_joined = models.DateTimeField(auto_now_add=True)


class Test(models.Model):
    pass