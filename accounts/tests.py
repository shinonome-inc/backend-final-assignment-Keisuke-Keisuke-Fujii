from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import SESSION_KEY, get_user_model
from django.conf import settings

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        # ユーザーがaccounts/signup/ のURLに訪れたという動作
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        # ↓ ユーザーがフォームにデータを打ち込んでユーザー登録ボタンを押した時の操作
        response = self.client.post(self.url, data)
        # assertRedirectsとは何か？
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(
            # モデル（user）.objects（モデルマネージャ（モデルを操作するもの））.モデルメソッド
            # モデルを操作（filterなど）する時にはobjectsが必要
            # モデルマネージャでモデルを操作した後はクエリセットかモデルインスタンスが返される
            # クエリセットが返された場合は（クエリセット）.モデルメソッドで後の操作できる．
            # モデルインスタンスなら（モデルインスタンス）.objects（モデルマネージャ（モデルを操作するもの））.モデルメソッド
            User.objects.filter(
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
        # ↑ response.contextはdict型でデータが入っており、その中のformを取ってきたい.
        # よってキーにformを指定することでformを取得.
        # responseで表示されている全てのhtml等の情報の中からform情報(キー)を取得.
        # ここのformはSignupViewのform_classに代入した SignupForm のインスタンスにあたる(モデルインスタンス).

        self.assertEqual(response.status_code, 200)
        user_record_count = User.objects.all().count()
        # 以下でUserテーブルのレコードは増えているか確認.
        self.assertEqual(user_record_count, User.objects.all().count())
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
        user_record_count = User.objects.all().count()
        # 以下でUserテーブルのレコードは増えているか確認.
        self.assertEqual(user_record_count, User.objects.all().count())
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
        user_record_count = User.objects.all().count()
        # 以下でUserテーブルのレコードは増えているか確認.
        self.assertEqual(user_record_count, User.objects.all().count())
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

        self.assertEqual(response.status_code, 200)
        user_record_count = User.objects.all().count()
        # 以下でUserテーブルのレコードは増えているか確認.
        self.assertEqual(user_record_count, User.objects.all().count())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password1"])
        self.assertIn("このフィールドは必須です。", form.errors["password2"])
        # ここをasserInでやるにはどうしたらよいか

    def test_failure_post_with_duplicated_user(self):
        pass

    def test_failure_post_with_invalid_email(self):
        pass

    def test_failure_post_with_too_short_password(self):
        pass

    def test_failure_post_with_password_similar_to_username(self):
        pass

    def test_failure_post_with_only_numbers_password(self):
        pass

    def test_failure_post_with_mismatch_password(self):
        pass


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
