from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import forms, views

# 逆引きなどのための名称はapp_name:nameなのでaccounts:signupなどとなる．
# プロジェクトmysiteのurlsからここに来て，もう一度URLを調べpath一覧に一致するurlがあればそのviewメソッド実行
app_name = "accounts"
urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path(
        "login/",
        LoginView.as_view(form_class=forms.LoginForm, template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("<str:username>/", views.UserProfileView.as_view(), name="user_profile"),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("<str:username>/unfollow/", views.UnFollowView.as_view(), name="unfollow"),
    path("<str:username>/following_list/", views.FollowingListView.as_view(), name="following_list"),
    path("<str:username>/follower_list/", views.FollowerListView.as_view(), name="follower_list"),
]
