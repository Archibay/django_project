from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'user_management'
urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),

]