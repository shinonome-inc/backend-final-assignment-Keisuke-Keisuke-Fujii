from django.conf import settings
from django.db import models

# get_user_model()でCustomUserを取得した方が良い？


class Tweet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="投稿者"
    )  # settings.AUTH_USER_MODELはCustomUserモデル
    content = models.TextField(max_length=140, verbose_name="ツイート内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="投稿日時")
