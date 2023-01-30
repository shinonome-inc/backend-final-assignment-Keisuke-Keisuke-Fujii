from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm

# SignUpViewではユーザ作成機能，作成されたユーザのログイン機能を実装する

# 汎用ビューの１つであるCreateViewを継承


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
        # 2つのform_validを実行．CCBV参照．このresponseには返り値であるHttpResponseRedirectが入る
        user = self.object  # CustomUserモデルのインスタンスを変数に格納
        login(self.request, user)
        """
        self.requestの中身はHttpReuqestオブジェクト.第2引数にログインさせたいユーザーインスタンス
        """
        return response  # success_urlにリダイレクト

    """
    formのバリデーション（form.is_valid()）がtrueだった場合に呼ばれるメソッドです。
    すなわち、formのところで見たように、バリデーションを通ったデータをもとに
    何かを実装したい時（ここではログイン処理を行う）はform_validメソッドを
    オーバーライドしていくことになります
    """
