from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import SESSION_KEY, get_user_model

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
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
        response = self.client.post(self.url, data)

        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(User.objects.filter(username=data["username"]).exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["username"])

        print(response.context)
        print(response.context["form"])

        print(form.errors)

    def test_failure_post_with_empty_username(self):
        pass

    def test_failure_post_with_empty_email(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass

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
