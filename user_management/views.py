from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.views import FormView
from django.urls import reverse_lazy

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
