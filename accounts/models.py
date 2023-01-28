from django.contrib.auth.models import AbstractUser
from django.db import models

"""
Djangoでは context という変数に、データベースから取ってきたデータが入るようになっています。
クラスベースビューではcontextに自動的に入り、get_context_data()というメソッドをオーバーライドすれば柔軟に色々なデータを入れることが可能
"""


class CustomUser(AbstractUser):
    # AbstractUserを継承してモデルをつくり，Emailフィールドのカラムを追加
    email = models.EmailField()


# class FriendShip(models.Model):
# pass
