from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.    

class University(models.Model):
    full_name = models.CharField(max_length=128, null=False, blank=False, verbose_name='Полное название')
    short_name = models.CharField(max_length=128, null=False, blank=False, verbose_name='Краткое название')
    foundation_date = models.DateField(null=False, blank=False, verbose_name='Дата Создания')

    def __str__(self) -> str:
        return self.short_name

    class Meta:
        verbose_name_plural = 'Университеты'  # множественное название
        verbose_name = 'Университет'  # в единственном числе
        ordering = ['full_name']


class Student(models.Model):
    fitst_name = models.CharField(max_length=64, blank=False, null=False, verbose_name='Имя')
    second_name = models.CharField(max_length=64, blank=False, null=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='Отчество')
    birth_date = models.DateField(blank=False, null=True, verbose_name='Дата Рождения')
    university = models.ForeignKey('University', null=False, on_delete=models.PROTECT, verbose_name='Университет')
    admission_date = models.DateField(blank=False, null=False, verbose_name='Дата поступления')

    class Meta:
        verbose_name_plural = 'Студенты'
        verbose_name = 'Студент'
        ordering = ['second_name']