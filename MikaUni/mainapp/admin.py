from django.contrib import admin

from .models import University, Student
from .forms import UniForm

# Register your models here.
# этот блок кода необходим для работы с административного сайта
# мы задаем как будут отображаться модели и какие модели будут видны с админки

class UniAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name', 'foundation_date')  # какие атрибуты класса отображать
    list_display_links = ('full_name', 'short_name')  
    search_fields = ('full_name', 'short_name', 'foundation_date') #  по каким атрибутам делать поиск
    form = UniForm


class StudentAdmin(admin.ModelAdmin):
    list_display = ('fitst_name', 'second_name', 'last_name', 'birth_date', 'university', 'admission_date')
    list_display_links = ('fitst_name', 'second_name', 'last_name', 'birth_date', 'university', 'admission_date')
    search_fields = ('fitst_name', 'second_name', 'last_name', 'university', 'admission_date')


admin.site.register(University, UniAdmin)   # регистрируем
admin.site.register(Student, StudentAdmin)
