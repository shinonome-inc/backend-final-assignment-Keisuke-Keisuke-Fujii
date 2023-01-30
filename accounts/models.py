from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # AbstractUserを継承してモデルをつくり，Emailフィールドのカラムを追加
    email = models.EmailField()


# class FriendShip(models.Model):
# pass
