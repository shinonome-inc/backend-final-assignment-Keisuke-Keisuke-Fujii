from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Tweet

CustomUser = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        # ログイン後の画面なのでログイン用テストユーザ作成
        # ログインするユーザのデータをモデルに追加して既存ユーザ扱いにする
        self.user1 = CustomUser.objects.create_user(
            username="testuser1",
            password="testpassword1",
            email="test1@example.com",
        )

        # ログインさせる
        self.client.login(username="testuser1", password="testpassword1")

        # home画面URL文字列の逆引き
        self.url = reverse("tweets:home")

        # ツイート投稿させる
        self.post = Tweet.objects.create(user=self.user1, content="testpost")

    def test_success_get(self):
        # context内に含まれるツイート一覧が、DBに保存されているツイート一覧と同一である
        # ↓ユーザーがtweets/home/ のURLに訪れているか確認
        response = self.client.get(self.url)  # プロフィールページURLに訪れる動作
        context = response.context

        self.assertEqual(response.status_code, 200)  # コード200なのを確認
        self.assertTemplateUsed(
            response, "tweets/home.html"
        )  # ホーム画面テンプレートhtmlが表示されているかを確認
        self.assertQuerysetEqual(context["tweet_list"], Tweet.objects.all())
        """
        レスポンスに想定通りのquerysetが含まれているか,全ユーザのツイート一覧とクエリが等しいか確認
        tweet_listはtweets/views.HomeViewのcontext_object_name
        """


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="testuser1",
            password="testpassword1",
            email="test1@example.com",
        )
        self.client.login(username="testuser1", password="testpassword1")
        self.url = reverse("tweets:create")

    def test_success_get(self):
        # Response Status Code: 200
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_create.html")

    def test_success_post(self):
        """
        ・Response Status Code: 302
        ・ホームにリダイレクトしている
        ・DBにデータが追加されている
        ・追加されたデータのcontentが送信されたcontentと同一である
        """

        test_tweet = {"content": "testtweet"}
        # test_tweetにTweetモデルのcontentフィールドに追加するためのtweetデータを格納
        response = self.client.post(self.url, test_tweet)
        """
        responseはユーザーがフォームにデータを打ち込んで送信した操作
        第二引数データtest_tweet(ツイート内容)を,第一引数のページであるself.url(SetUpメソッドで定めた)にある
        フォームで送る操作を示す.
        """

        # responseにより登録されたデータが存在していることを確認
        self.assertRedirects(
            response,  # responseという操作（インスタンス？）が，
            reverse("tweets:home"),  # ツイート成功後のURLへ
            status_code=302,  # リダイレクトが成功し
            target_status_code=200,  # 画面表示もOKである
        )
        # test_tweetがTweetモデルのcontentフィールドに存在しているか確認
        self.assertTrue(Tweet.objects.filter(content=test_tweet["content"]).exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_content(self):
        """
        ・Response Status Code: 200
        ・フォームに適切なエラーメッセージが含まれている
        ・DBにレコードが追加されていない
        """
        test_empty_content_tweet = {"content": ""}
        response = self.client.post(self.url, test_empty_content_tweet)
        self.assertEqual(response.status_code, 200)

        # 内容が空白のツイートがTweetモデルのcontentフィールドに存在していないことを確認
        self.assertFalse(
            Tweet.objects.filter(content=test_empty_content_tweet["content"]).exists()
        )
        # responseで表示されている全てのhtml等の情報の中からform情報(ディクショナリのキー)を取得.
        form = response.context["form"]
        self.assertIn("このフィールドは必須です。", form.errors["content"])

    def test_failure_post_with_too_long_content(self):
        pass


class TestTweetDetailView(TestCase):
    def test_success_get(self):
        pass


class TestTweetDeleteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
