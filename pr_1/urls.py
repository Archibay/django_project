from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'pr_1'
urlpatterns = [
    path('detail/', views.detail_view, name='detail'),

]
