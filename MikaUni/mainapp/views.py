from typing import Any, Dict
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError

from .models import University, Student
from .forms import UniForm, StudentForm


# Create your views here.

# контроллер функция главной страницы
def mainpage(request: HttpRequest) -> HttpResponse:
    # получаем список универов
    unis = University.objects.all()

    # упаковываем в словарь контекста и передаем
    context = {'unis': unis}

    # 'mainapp/mainpage.html' - шаблон
    return render(request, 'mainapp/mainpage.html', context)


# котроллер функция - выводим студентов в соответствии с универом
def by_uni(request: HttpRequest, uni_id: int) -> HttpResponse:
    # получаем всех студентов отфильтрованнаях по внешнему ключу индекса универа uni_id
    students =  Student.objects.filter(university=uni_id)

    # получаем объект текущего универа
    current_uni = University.objects.get(pk=uni_id)

    # заполняем контекст и рендерим
    context = {'students': students, 'current_uni': current_uni}
    
    return render(request, 'mainapp/by_uni.html', context)


########## формы для работы со студентами
  

# контроллер добавления студентов
def add_student(request: HttpRequest, uni_id: int) -> HttpResponse:
    if request.method == 'POST':  # если мы получили отправленный текст
        student_form = StudentForm(request.POST)  # снимаем с формы данные
        if student_form.is_valid():  # если форма заполнена корректно, пролетаем внутрь
            student = student_form.save()  # сохраняем новый объект
            students =  Student.objects.filter(university=uni_id)  # получаем список студентов по индексу универа
            current_uni = University.objects.get(pk=uni_id)  # получаем объект текущего универа
            context = {'students': students, 'current_uni': current_uni}  # запихиваем в контекст и рендерим

            # делаем переадресацию, иначе почему-то форма при обновлении отправляет повторно
            return redirect("by_uni", uni_id=current_uni.pk) 
        else: # если форма заполнена с ошибками - возвращаем
            current_uni = University.objects.get(pk=uni_id)  # получаем объект текущего универа
            context = {'form': student_form, 'current_uni': current_uni} # запихиваем в контекст и переотправляем форму
            return render(request, 'mainapp/add_student.html', context)
    else: # значит контроллер обращается получить форму
        student_form = StudentForm()  # получае пустую форму
        current_uni = University.objects.get(pk=uni_id)  # получаем объект текущего универа
        context = {'form': student_form, 'current_uni': current_uni} # пихаем в контекст и отправляе форму
        return render(request, 'mainapp/add_student.html', context)
    

# контроллер обновления данных о студенте
def edit_student(request: HttpRequest, uni_id: int, student_id: int) -> HttpResponse:
    if request.method == 'POST':  # если получаем отправку
        student = Student.objects.get(pk=student_id) # получае объект студента
        student_form = StudentForm(request.POST, instance=student)  # снимаем данные с формы и привязываем к объекту
        if student_form.is_valid():  # если все корректно - обрабатываем
            student_form.save()  # сохраняем изменения
            students =  Student.objects.filter(university=uni_id)  # получаем студентов текущего универа
            current_uni = University.objects.get(pk=uni_id)  #получаем объект текущего универа
            context = {'students': students, 'current_uni': current_uni}
            return redirect("by_uni", uni_id=current_uni.pk)  # только так
        else:  # если форма заполнена не верно - отправляем заново
            current_uni = University.objects.get(pk=uni_id)
            context = {'form': student_form, 'current_uni': current_uni, 'student_id': student_id}
            return render(request, 'mainapp/edit_student.html', context)
    else: # обращаемся получить форму - метод: GET
        current_student = Student.objects.get(pk=student_id)  # получаем данные о студенте

         # предварительно заполняем форму текущими данными 
         # это делает передачей в форму атрибута `instance=current_student`
        student_form = StudentForm(instance=current_student) 
        current_uni = University.objects.get(pk=uni_id) # получаем объект текущего универа
        context = {'form': student_form, 'current_uni': current_uni, 'student_id': student_id}
        return render(request, 'mainapp/edit_student.html', context)  # рендерим форму для заполнения
            
    
def delete_student(request: HttpRequest, uni_id: int, student_id: int) -> HttpResponse:
    student = Student.objects.get(pk=student_id)  # получаем объект студента
    if request.method == 'POST':  # 
        student.delete() # удаляем
        students =  Student.objects.filter(university=uni_id)  # получаем список студентов по внешнему ключу универа
        current_uni = University.objects.get(pk=uni_id)  # получаем объекь текущего универа 
        context = {'students': students, 'current_uni': current_uni}  # 
        return redirect("by_uni", uni_id=current_uni.pk)
    else:
        context = {'student': student}
        return render(request, 'mainapp/delete_student.html', context)

        
################## формы для работы с Университетами


class UniCreateView(CreateView):
    template_name = 'mainapp/add_uni.html'
    form_class = UniForm
    success_url = reverse_lazy('mainpage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

def delete_uni(request: HttpRequest, uni_id: int) -> HttpResponse:
    uni = University.objects.get(pk=uni_id)
    # помним, у нас стоит ограничение на внешний ключ!
    # поэтому у нас при удалении помжет выскочить ошибка 
    # связанная с ограничением, ее мы и поймаем 
    # ::: ошибка выскочит, если в университете хотя бы один студент
    try:
        if request.method == 'POST':
            uni.delete()
            return redirect("mainpage")
        else:
            # подсчитаем количество студентов в текущем универе
            students_num = Student.objects.filter(university=uni_id).count()  
            context = {'uni': uni, 'students_num': students_num}
            return render(request, 'mainapp/delete_uni.html', context)
    except ProtectedError:
        messages.add_message(request, messages.ERROR, 'Нельзя удалить, т.к. есть студенты')
        return redirect("mainpage")
    

def edit_uni(request: HttpRequest, uni_id: int) -> HttpResponse:
    if request.method == "POST":
        uni = University.objects.get(pk=uni_id)
        uni_form = UniForm(request.POST, instance=uni)
        if uni_form.is_valid():
            uni_form.save()
            uni = University.objects.get(pk=uni_id)
            students =  Student.objects.filter(university=uni_id)
            context = {'students': students, 'current_uni': uni}
            return redirect("by_uni", uni_id=uni.pk)
        else:
            uni = University.objects.get(pk=uni_id)
            context = {'form': uni_form, 'uni': uni}
            return render(request, 'mainapp/edit_uni.html', context=context)
    else:
        uni = University.objects.get(pk=uni_id)
        uni_form = UniForm(instance=uni)
        context = {'form': uni_form, 'uni': uni}
        return render(request, 'mainapp/edit_uni.html', context=context)
