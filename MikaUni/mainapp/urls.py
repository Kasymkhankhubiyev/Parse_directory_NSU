from django.urls import path, include

from .import views

# app_name = 'mainapp'
urlpatterns = [
    path("<int:uni_id>/", views.by_uni, name='by_uni'),
    path("", views.mainpage, name='mainpage'),
    # path('accounts/login/', views.LoginView, name='login'),
]