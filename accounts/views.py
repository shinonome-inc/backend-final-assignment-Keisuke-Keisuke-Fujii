from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from tweets.models import Tweet

from .forms import SignupForm

CustomUser = get_user_model()

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


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = "accounts/profile.html"
    model = CustomUser
    context_object_name = "profile"
    slug_field = "username"  # モデルのフィールドの名前
    slug_url_kwarg = "username"  # urls.pyでのキーワードの名前すなわち任意のユーザ名

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context["tweet_list"] = (
            Tweet.objects.select_related("user")
            .filter(user=user)
            .order_by("-created_at")
        )
        return context
