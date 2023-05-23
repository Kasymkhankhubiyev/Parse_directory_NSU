from django.forms import ModelForm

from .models import University, Student

class UniForm(ModelForm):
    class Meta:
        model = University
        fields = ('full_name', 'short_name', 'foundation_date')


class StudentForm(ModelForm):
    class Meta: 
        model = Student
        fields = ('fitst_name', 'second_name', 'last_name', 'birth_date', 'university', 'admission_date')