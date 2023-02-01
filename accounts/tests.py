from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

# from django.conf import settings

CustomUser = get_user_model()


class TestSignupView(TestCase):
    # test用のログインデータ
    def setUp(self):
        # アカウントを登録するurlページへの逆引き
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        # ユーザーがaccounts/signup/ のURLに訪れそのテンプレートhtmlが表示されているかを確認
        response = self.client.get(self.url)  # accounts/signup/ のURLに訪れる動作

        self.assertEqual(response.status_code, 200)  # コード200なのを確認
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        """
        responseはユーザーがフォームにデータを打ち込んでユーザー登録ボタンを押した操作
        第二引数データdataを持って,第一引数のurlであるself.url（SetUpメソッドで定めたsignup成功時の遷移先url）に
        遷移する操作を示す
        """
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, data)

        self.assertRedirects(
            response,  # responseという操作（インスタンス？）が，
            reverse("tweets:home"),  # reverse逆引URL(tweets:home)へ
            status_code=302,  # ちゃんとリダイレクトという動きが行われ
            target_status_code=200,  # 画面表示がOKである
        )  # responseにより登録されたデータが存在していることを確認
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


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


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
