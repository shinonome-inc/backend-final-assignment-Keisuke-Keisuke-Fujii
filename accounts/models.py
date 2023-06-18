from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # AbstractUserを継承してモデルをつくり，Emailフィールドのカラムを追加
    email = models.EmailField()


class FriendShip(models.Model):
    """
    related_nameでORMで参照できるようにする。
    1つのモデルに対し複数のForeignKeyフィールドを設定する場合このオプションが必須
    フィールドがfollower=Kei, following=Kyokoというレコードがあったら、
    「KeiがKyokoのことをフォローすることでKyokoのフォロワーになっているという関係」
    を示す。followingはfolloweeの方がわかりやすいかも

    なお、related_nameはターミナルのシェル(python manage.py shell)操作などで用いる。
    フィールド名と逆なのに注意。
    シェルの書き方
    from accounts.models import CustomUser (FriendShipの親モデル)
    user=CustomUser.objects.get(username="Kyoko") なおKyokoのid=2
    user.following.all()
    ↑このfollowingはrelated_nameでFriendShipのDBとは逆にこちらは素直に
    user(Kyoko)「が」フォローしている(FriendShipモデルのfollowerフィールドがKyokoである)FriendShipオブジェクトを抽出

    user.follower.all()
    ↑このfollowerはrelated_nameでFriendShipのDBとは逆にこちらは素直に
    user(Kyoko)「を」フォローしている(FriendShipモデルのfollowingフィールドがKyokoである)オブジェクト抽出
    """

    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="follower")
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
