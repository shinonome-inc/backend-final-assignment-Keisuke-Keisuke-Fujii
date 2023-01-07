from django.shortcuts import render
from django.contrib.auth import login  # authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    # ↑ forms.pyで記載したクラスであるSignUpFormを適用したい
    template_name = "accounts/signup.html"
    # ↑ SignUpViewを表示するhtmlファイル名で,代入したhtmlファイルがそのViewで表示されるhtmlファイルとなる.
    success_url = reverse_lazy("tweets:home")
    # ↑ ユーザ作成成功後にリダイレクトされる先
    """
    クラス変数の段階では、urls.pyが読み込まれておらず、urlを読み込む（URLの逆引き）時にエラーが生じてしまう。
    reverse_lazyで遅延評価することによって、urls.pyが読み込まれた後に評価でき、URLの逆引きができる
    """

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response
