# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
)

from .forms import TweetForm
from .models import Tweet

# サインアップにおけるリダイレクト先の画面としてHomeView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"


class TweetCreateView(LoginRequiredMixin, CreateView):
    # 属性はこの順番でないとエラー起こる.
    template_name = "tweets/tweet_create.html"
    form_class = TweetForm
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        # 現在ログインしているユーザーを代入
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = "tweets/tweet_detail.html"
    context_object_name = "tweet"


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "tweets/tweet_delete.html"
    model = Tweet
    success_url = reverse_lazy("tweets:home")

    # 作成者がログイン中のユーザか検証.test_func()メソッドの返り値がFalseならpermission errorでリクエスト拒否.
    def test_func(self):
        current_user = self.request.user
        tweet_user = self.get_object().user  # Tweetモデルのuser属性を得る
        return current_user == tweet_user
