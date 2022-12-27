from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.views import FormView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from user_management.forms import RegistrationForm


class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('blog:posts_all')

    def form_valid(self, form):
        user = form.save()
        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/user_detail.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'registration/user_update.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        user = self.request.user
        return user

