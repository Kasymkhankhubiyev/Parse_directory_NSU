from django.urls import path, include

from .import views

# app_name = 'mainapp'
urlpatterns = [
     #  ссыла на контроллер-класс добавление универстета
    path('add_uni/', views.UniCreateView.as_view(), name='AddUni'), 

    # ссылка на контроллер-функцию добавление студента
    # uni_id - индекс универа
    # индекс - это ключ - primary key
    path('<int:uni_id>/add_student/', views.add_student, name='AddStudent'), 

    # ссылка на контроллер-функцию редактирование универа
    # uni_id - индекс универа
    path('<int:uni_id>/edit_university/', views.edit_uni, name='EditUni'), 

    # ссылка на котроллер-функциб удалить универ
    # uni_id - индекс универа
    path('<int:uni_id>/delete_university/', views.delete_uni, name='DelUni'), 

    # ссылка на котроллер функцию редактировать студента
    # uni_id - индекс универа
    # student_id - индекс студента
    path('<int:uni_id>/edit_student/<int:student_id>', views.edit_student, name='EditStudent'),

    # ссылка на котрллер функцию удалить студента
    # uni_id - индекс универа
    # student_id - индекс студента
    path('<int:uni_id>/delete_student/<int:student_id>', views.delete_student, name='DelStudent'),

    # индексированная ссылка на контроллер класс визуализации списка студентов по универу.
    # uni_id - индекс универа
    path("<int:uni_id>/", views.by_uni, name='by_uni'), 

    # ссылка на главную страниыу со списокм универов
    path("", views.mainpage, name='mainpage'),  #
]