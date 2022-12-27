from django.urls import include, path
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . import views


app_name = 'user_management'
urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),

    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("user-detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("user-update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
]
