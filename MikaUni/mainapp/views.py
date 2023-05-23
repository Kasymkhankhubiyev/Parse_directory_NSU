from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
# from .forms import UserLogInForm
from .models import University, Student

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.

def mainpage(request: HttpRequest) -> HttpResponse:
    # students = Student.objects.all()
    unis = University.objects.all()
    context = {'unis': unis}
    return render(request, 'mainapp/mainpage.html', context)


def by_uni(request: HttpRequest, uni_id: int) -> HttpResponse:
    students =  Student.objects.filter(university=uni_id)
    unis = University.objects.all()
    current_uni = University.objects.get(pk=uni_id)
    context = {'students': students, 'unis': unis, 'current_uni': current_uni}
    
    return render(request, 'mainapp/by_uni.html', context)
