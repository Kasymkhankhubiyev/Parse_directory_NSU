from django.contrib import admin

from .models import University, Student

# Register your models here.

class UniAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_name', 'foundation_date')
    list_display_links = ('full_name', 'short_name')
    search_fields = ('full_name', 'short_name', 'foundation_date')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('fitst_name', 'second_name', 'last_name', 'birth_date', 'university', 'admission_date')
    list_display_links = ('fitst_name', 'second_name', 'last_name', 'birth_date', 'university', 'admission_date')
    search_fields = ('fitst_name', 'second_name', 'last_name', 'university', 'admission_date')


admin.site.register(University, UniAdmin)
admin.site.register(Student, StudentAdmin)
