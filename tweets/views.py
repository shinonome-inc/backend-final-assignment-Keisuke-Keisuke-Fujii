# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# サインアップにおけるリダイレクト先の画面としてHomeView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"
