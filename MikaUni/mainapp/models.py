from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.    

# модель Университета в базе данных
class University(models.Model):
    """
    max_length=128 - устанавливаем максимальную длину текстового поля
    если null=False - недопускается устанавливать Null, 
    если blank=False - нельзя оставлять пустым
    если unique=True - следим за уникальностью - хотим, чтобы университеты были уникальными
    verbose_name - человеческое название - в административном сайте будет высвечиваться под этим названием
    """
    # полное наименование ВУЗа
    full_name = models.CharField(max_length=128, null=False, blank=False, verbose_name='Полное название', unique=True)
    short_name = models.CharField(max_length=128, null=False, blank=False, verbose_name='Краткое название')
    foundation_date = models.DateField(null=False, blank=False, verbose_name='Дата Создания')

    def __str__(self) -> str:
        # строковое представление объекта, 
        # нужно прежде всего для административного сайта
        return self.short_name

    class Meta:
        verbose_name_plural = 'Университеты'  # множественное название
        verbose_name = 'Университет'  # в единственном числе
        ordering = ['full_name']  # сортировка по полному названию по возврастанию


# модель студента в базе данных
class Student(models.Model):
    fitst_name = models.CharField(max_length=64, blank=False, null=False, verbose_name='Имя')
    second_name = models.CharField(max_length=64, blank=False, null=False, verbose_name='Фамилия')
    last_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='Отчество')
    birth_date = models.DateField(blank=False, null=True, verbose_name='Дата Рождения')  # поле даты
    # ссылаемся на университет - свящь один-ко многим - 
    # каждой записи из таблицы университета - соответствую какое-то кол-во студентов 
    # constarint - ограничение - если есть студенты, ссылающиеся на универ - удалять нельзя 
    # за это отвечает пункт `on_delete=models.PROTECT`
    university = models.ForeignKey(University, null=False, on_delete=models.PROTECT, verbose_name='Университет')
    admission_date = models.DateField(blank=False, null=False, verbose_name='Дата поступления')

    class Meta:
        verbose_name_plural = 'Студенты'
        verbose_name = 'Студент'
        ordering = ['second_name', 'fitst_name']  # Сортируем сначала по фамилии потом по имени - по возрастанию