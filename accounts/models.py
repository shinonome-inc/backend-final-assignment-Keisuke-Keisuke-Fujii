from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # AbstractUserを継承してモデルをつくり，Emailフィールドのカラムを追加
    email = models.EmailField()


class FriendShip(models.Model):
    """
    related_nameでORMで参照できるようにする。
    1つのモデルに対し複数のForeignKeyフィールドを設定する場合このオプションが必須
    """

    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "フォロワー/フォロー"
        constraints = [
            # 複合ユニーク制約、filedsに指定したカラムの値が同じレコードの存在を許可しない
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_friendship",
            )
        ]

        def __str__(self):
            return f"{self.follower} → {self.following}"
