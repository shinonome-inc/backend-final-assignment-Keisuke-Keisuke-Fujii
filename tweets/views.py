# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"
    context_object_name = "tweets"
    # queryset = Tweet.objects.select_related("user").order_by("-created_at")
