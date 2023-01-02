from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        # username = form.cleaned_data["username"]
        # password = form.cleaned_data["password1"]
        user = form.save()
        """ 
        user = authenticate(self.request, userame=username, password=password 
        であったが
        フォームを保存するときにすでにユーザーを取得しているので、
        login()を呼び出すときにすでにバックエンドを提供しているため、
        authenticateを呼び出す必要はない
        """
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return response
