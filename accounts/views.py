from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView

from .forms import LoginForm, SignupForm

# SignUpViewではユーザ作成機能，作成されたユーザのログイン機能を実装する

# 汎用ビューの１つであるCreateViewを継承


class SignupView(CreateView):
    form_class = SignupForm
    # ↑ forms.pyで記載したクラスであるSignUpFormを適用したい
    template_name = "accounts/signup.html"
    # ↑ SignUpViewを表示するhtmlファイル名で,代入したhtmlファイルがそのViewで表示されるhtmlファイルとなる.
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    # ↑ ユーザ作成成功後にリダイレクトされる先

    def form_valid(self, form):
        response = super().form_valid(form)  # ここのフォームは何？
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
