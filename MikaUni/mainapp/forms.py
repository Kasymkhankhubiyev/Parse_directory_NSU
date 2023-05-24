from django.forms import ModelForm, ModelChoiceField

from .models import University, Student


# форма для добавления университета
class UniForm(ModelForm):
    class Meta:
        model = University  # привязываем модель к форме
        fields = '__all__'  # берем все стобцы


# форма для записи студента
class StudentForm(ModelForm):
    # хотим вставлять только из сущесвующих университетов,\ 
    # поэтому делаем поля с выбором, и чтобы запретить пустое значение устанавлиавем empty_label=None
    university = ModelChoiceField(queryset=University.objects.all(), label='Университет', empty_label=None)
    class Meta: 
        model = Student  # привязываем модель к форму
        fields = ('fitst_name', 'second_name', 'last_name', 'birth_date', 'university', 'admission_date')