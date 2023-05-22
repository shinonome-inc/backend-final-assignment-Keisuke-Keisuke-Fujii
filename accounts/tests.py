from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet

from .models import FriendShip

CustomUser = get_user_model()


class TestSignupView(TestCase):
    # test用のログインデータ
    def setUp(self):
        # アカウントを登録するurlページへの逆引き文字列
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        # ユーザーがaccounts/signup/ のURLに訪れそのテンプレートhtmlが表示されているかを確認
        response = self.client.get(self.url)  # accounts/signup/ のURLに訪れる動作

        self.assertEqual(response.status_code, 200)  # コード200なのを確認
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        """
        responseはユーザーがフォームにデータを打ち込んでユーザー登録ボタンを押し送信した操作
        第二引数データdataを,第一引数のurlページであるself.url（SetUpメソッドで定めたsignupフォームのあるurl）にある
        フォームで送る操作を示す
        """
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, data)

        # responseにより登録されたデータが存在していることを確認
        self.assertRedirects(
            response,  # responseという操作（インスタンス？）が，
            reverse(settings.LOGIN_REDIRECT_URL),  # reverse逆引URL(LOGIN_REDIRECT_URL=tweets:home)へ
            status_code=302,  # ちゃんとリダイレクトという動きが行われ
            target_status_code=200,  # 画面表示がOKである
        )
        self.assertTrue(
            CustomUser.objects.filter(
                username=data["username"],
            ).exists()
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        form_empty_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, form_empty_data)
        # ↑ responseで表示されているhtml等の情報を全ていれる.dict型.
        form = response.context["form"]
        # responseで表示されている全てのhtml等の情報の中からform情報(キー)を取得.
        # ここのformはSignupViewのform_classに代入した SignupForm のインスタンスにあたる(モデルインスタンス).
        # ここで何してるか正直わからない

        self.assertEqual(response.status_code, 200)
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])
        self.assertIn("このフィールドは必須です。", form.errors["email"])
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])
        # ここのasserInをきれいにしたい

    def test_failure_post_with_empty_username(self):
        username_empty_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, username_empty_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])

    def test_failure_post_with_empty_email(self):
        email_empty_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, email_empty_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["email"])

    def test_failure_post_with_empty_password(self):
        password_empty_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, password_empty_data)
        form = response.context["form"]
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])
        # ここをきれいにするにはどうしたらよいか
        # パスワードの片方のフォームだけ入力された場合どうなるの？

    def test_failure_post_with_duplicated_user(self):
        # 既に存在するデータ
        existing_user_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        # 既に存在するデータとしてexistingを作成.作成は問題なく可能.
        response = self.client.post(self.url, existing_user_data)
        self.assertTrue(
            CustomUser.objects.filter(
                username=existing_user_data["username"],
            ).exists()
        )
        # もう一度同じデータでユーザ作成
        response = self.client.post(self.url, existing_user_data)

        # CustomUser.objects.all().count() == 1
        self.assertEqual(CustomUser.objects.all().count(), 1)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("同じユーザー名が既に登録済みです。", form.errors["username"])

    def test_failure_post_with_invalid_email(self):
        email_invalid_data = {
            "username": "testuser",
            "email": "invalid_email",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, email_invalid_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("有効なメールアドレスを入力してください。", form.errors["email"])

    def test_failure_post_with_too_short_password(self):
        too_short_password_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "short",
            "password2": "short",
        }
        response = self.client.post(self.url, too_short_password_data)
        print(response)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password2"])

    def test_failure_post_with_password_similar_to_username(self):
        password_similar_to_username_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testuser1",
            "password2": "testuser1",
        }
        response = self.client.post(
            self.url,
            password_similar_to_username_data,
        )
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password2"])
        # パスワードが空白の時はpassword1とpassword2両方でエラーが出ていたのにここはなぜ2だけエラー？

    def test_failure_post_with_only_numbers_password(self):
        only_numbers_password_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "875329948",
            "password2": "875329948",
        }
        response = self.client.post(
            self.url,
            only_numbers_password_data,
        )
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは数字しか使われていません。", form.errors["password2"])

    def test_failure_post_with_mismatch_password(self):
        with_mismatch_password_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "fdasjkn2",
            "password2": "novcian2",
        }
        response = self.client.post(
            self.url,
            with_mismatch_password_data,
        )
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        # 以下でCustomUserテーブルのレコードは増えていないことを確認.
        self.assertEqual(CustomUser.objects.all().count(), 0)
        self.assertFalse(form.is_valid())
        self.assertIn("確認用パスワードが一致しません。", form.errors["password2"])


class TestUserLoginView(TestCase):
    def setUp(self):
        # ログインフォームのあるurlページへの逆引き
        self.url = reverse(settings.LOGIN_URL)
        # ログインするユーザのデータをモデルに追加して既存ユーザ扱いにする
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )

    def test_success_get(self):
        # ユーザーがaccounts/login/ のURLに訪れそのテンプレートhtmlが表示されているかを確認
        response = self.client.get(self.url)  # accounts/login/ のURLに訪れる動作

        self.assertEqual(response.status_code, 200)  # コード200なのを確認
        self.assertTemplateUsed(response, "accounts/login.html")  # ログインテンプレートhtmlが表示されているかを確認

    def test_success_post(self):
        login_success_post_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(self.url, login_success_post_data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        not_exists_user_data = {
            "username": self.user.username + "aiueo",
            "password": self.user.password,
        }
        response = self.client.post(self.url, not_exists_user_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
            form.errors["__all__"],
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        empty_password_data = {
            "username": self.user.username,
            "password": "",
        }
        response = self.client.post(self.url, empty_password_data)
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password"])
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserLogoutView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.client.login(username="testuser", password="testpassword")

    def test_success_post(self):
        response = self.client.post(reverse("accounts:logout"))  # どのような処理の実行内容
        # （ローカルホスト）/accounts/logoutへのリクエストがあると，/accounts/loginに連れていくようになっている
        # djangoのデフォルトのLogoutViewにて，ログアウトした時はsettings.LOGOUT_REDIRECT_URLに連れていくようになっている
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),  # どのような処理の実行結果
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        # ログイン後の画面なのでログイン用テストユーザ作成
        # ログインするユーザのデータをモデルに追加して既存ユーザ扱いにする
        self.user1 = CustomUser.objects.create_user(
            username="testuser1",
            password="testpassword1",
            email="test1@example.com",
        )

        # フォロー機能テストのためself.user2を作る
        self.user2 = CustomUser.objects.create_user(
            username="testuser2",
            password="testpassword2",
            email="test2@example.com",
        )

        # ログインさせる
        self.client.login(username="testuser1", password="testpassword1")

        # プロフィール画面url文字列の逆引き
        self.url = reverse(
            "accounts:user_profile", kwargs={"username": self.user1.username}
        )  # urls.pyでstr:usernameとなっているのでキーはusernameになる。

        # ツイート投稿させる
        Tweet.objects.create(user=self.user1, content="testpost")

        # user1がuser2をフォローする
        FriendShip.objects.create(follower=self.user1, following=self.user2)

        # user2がuser1をフォローする
        FriendShip.objects.create(follower=self.user2, following=self.user1)

    def test_success_get(self):
        """
        ツイート機能テスト時
        品質:該当ユーザーのツイート一覧取得
        効果:context内に含まれるツイート一覧が、DBに保存されている該当のユーザーのツイート一覧と同一である

        フォロー機能テスト時
        品質:該当ユーザーのフォロー数・フォロワー数を表示する。
        効果:context内に含まれるフォロー数とフォロワー数が
        DBに保存されている該当のユーザーのフォロー数とフォロワー数に同一である
        """
        # ↓ユーザーがaccounts/<str:username>/ のURLに訪れているか確認
        response = self.client.get(self.url)  # プロフィールページURLに訪れる動作

        # プロフィール画面に存在する全てのcontextすなわち特定ユーザのツイートやフォロー数などの全ての要素
        context = response.context

        self.assertEqual(response.status_code, 200)  # コード200なのを確認
        self.assertTemplateUsed(response, "accounts/profile.html")  # プロフィールテンプレートhtmlが表示されているかを確認
        self.assertQuerysetEqual(context["tweet_list"], Tweet.objects.filter(user=self.user1))
        self.assertEqual(context["following_count"], FriendShip.objects.filter(follower=self.user1).count())
        self.assertEqual(context["follower_count"], FriendShip.objects.filter(following=self.user1).count())
        """
        レスポンスに想定通りのquerysetが含まれているか,全ユーザのツイート一覧とクエリが等しいか確認
        tweet_listはaccounts/views.UserProfileViewのget_context_data内のcontext[tweet_list]
        context["tweet_list"]はプロフィール画面で表示されるツイート一覧のコンテキスト形式
        context["following_count"]はフォロー数
        FriendShip.objects.filter(follower=self.user1).count()は自分がフォロワーになっているFriendShipモデルのオブジェクトの数
        """


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
