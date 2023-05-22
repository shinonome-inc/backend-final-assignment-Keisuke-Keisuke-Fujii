from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from tweets.models import Tweet

from .forms import SignupForm
from .models import FriendShip

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

        # テンプレートで表示されているユーザ
        user = self.object
        context["tweet_list"] = Tweet.objects.select_related("user").filter(user=user).order_by("-created_at")

        # filter(follower=user)は,モデルのfollower変数にuserを格納してモデルのfollowerフィールドの該当ユーザに絞る.
        # フォロー数==自分がフォロワーになっている数
        # フォロワー数==自分がフォローされている数
        context["following_count"] = FriendShip.objects.filter(follower=user).count()
        context["follower_count"] = FriendShip.objects.filter(following=user).count()

        # self.request.userは現在ログインして画面を閲覧しているユーザ。request.userはHTTPrequestを送るユーザという意味。login_user
        # userはtemplateで表示しているユーザ。template_user
        context["login_user_follows_template_user"] = FriendShip.objects.filter(
            following=user, follower=self.request.user
        ).exists()
        context["template_user_follows_login_user"] = FriendShip.objects.filter(
            following=self.request.user, follower=user
        ).exists()
        context["mutual_follow"] = FriendShip.objects.filter(
            Q(following=user, follower=self.request.user) & Q(following=self.request.user, follower=user)
        ).exists()

        return context


class FollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follow.html"
    model = FriendShip

    # HTTP POSTリクエストを処理。この時のリクエストはフォローをするという動作
    def post(self, request, *args, **kwargs):
        # リクエストを送信（フォロー申請）したユーザを格納
        follower = self.request.user

        # フォロー申請されたユーザを格納
        # POSTで送信されたusername(ユーザ名)をもつCustomUserモデルオブジェクトが見つかればそれを取得。
        # オブジェクトが見つからない場合、404エラーを返す。
        following = get_object_or_404(CustomUser, username=self.kwargs["username"])

        # ユーザーが自分自身をフォローしようとしている場合の処理を行う。
        if following == follower:
            # メッセージフレームワークによる様々なメッセージを出す
            messages.warning(request, "自分自身はフォローできません。")

            # 失敗したので特定の画面に戻す。メッセージを表示させるのでレンダリングで戻す？
            return render(request, "tweets/home.html")

        # すでにフォローしている場合の処理を行う
        elif FriendShip.objects.filter(following=following, follower=follower).exists():
            messages.warning(request, f"すでに { following.username } さんをフォローしています。")
            return render(request, "tweets/home.html")

        # 新しいフォロー関係を作成する(フォロー成功)
        else:
            FriendShip.objects.create(following=following, follower=follower)
            messages.success(request, f"{ following.username } さんをフォローしました。")

            # フォロー後にユーザーをホーム画面にリダイレクトする
            """
            return HttpResponseRedirect(reverse_lazy("tweets:home"))
            return render(request, "accounts/follow.html")のどちらか
            """
            return render(request, "tweets/home.html")


class UnFollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/unfollow.html"
    model = FriendShip

    def post(self, request, *args, **kwargs):
        follower = self.request.user
        following = get_object_or_404(CustomUser, username=self.kwargs["username"])

        # セイウチ演算子(Walrus operator)を用い、セイウチ演算子：代入文 → 代入式として使えるようにした
        # 特にif文においては、代入と評価を同時に行うことが出来るようになる。
        if friend := FriendShip.objects.filter(following=following, follower=follower):
            friend.delete()
            messages.success(request, f"{ following.username } さんのフォローを解除しました。")
            return render(request, "tweets/home.html")

        else:
            messages.warning(request, "フォローしていない人や、自分自身をフォロー解除できません。")
            return render(request, "tweets/home.html")


class FollowingListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.kwargs["username"]
        context["following_list"] = (
            FriendShip.objects.select_related("following")
            .filter(follower__username=self.kwargs["username"])
            .order_by("-created_at")
        )
        return context


class FollowerListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.kwargs["username"]
        context["follower_list"] = (
            FriendShip.objects.select_related("follower")
            .filter(following__username=self.kwargs["username"])
            .order_by("-created_at")
        )
        return context
