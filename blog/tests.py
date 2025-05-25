from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Author
from django.utils import timezone


class PostListEndpointTests(APITestCase):
    def setUp(self):
        # Create test user and author
        self.test_user = User.objects.create_user(
            username="testuser", email="test_user@example.com", password="testpassword"
        )
        self.test_author = Author.objects.create(
            name="Test Author", email="test_author@example.com", user=self.test_user
        )
        Post.published_date.auto_now_add = False
        # Create test post dated today
        Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.test_author,
            active=True,
            published_date=timezone.now(),
        )

        # Create test post dated yesterday
        Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.test_author,
            active=True,
            published_date=timezone.now() - timezone.timedelta(days=1),
        )

        # Create test post dated 2 weeks ago
        Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.test_author,
            active=True,
            published_date=timezone.now() - timezone.timedelta(weeks=2),
        )

        # Create test post dated today
        Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.test_author,
            active=False,
            published_date=timezone.now(),
        )

        # Create test post dated yesterday
        Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.test_author,
            active=False,
            published_date=timezone.now() - timezone.timedelta(days=1),
        )

        # Create test post dated 2 weeks ago
        Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.test_author,
            active=False,
            published_date=timezone.now() - timezone.timedelta(weeks=2),
        )

    def test_list_posts_return_active(self):
        url = reverse("post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_posts_return_active ======================"
        )
        print(post_results)
        print(
            "====================== end test_list_posts_return_active ======================"
        )

        # assert that all post results is active
        self.assertTrue(
            any(post["active"] == True for post in post_results),
            "Some post returned is not active",
        )

    def test_list_post_filter_by_active(self):
        url = reverse("post-list")
        response = self.client.get(url, {"active": "true"})
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_post_filter_by_active ======================"
        )
        print(post_results)
        print(
            "====================== end test_list_post_filter_by_active ======================"
        )

        # assert that all post results is active
        self.assertTrue(
            all(post["active"] == True for post in post_results),
            "Not all posts returned are active",
        )

    def test_list_post_filter_by_inactive(self):
        url = reverse("post-list")
        response = self.client.get(url, {"active": "false"})
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_post_filter_by_inactive ======================"
        )
        print(post_results)
        print(
            "====================== end test_list_post_filter_by_inactive ======================"
        )

        # assert that all post results is inactive
        self.assertTrue(
            all(post["active"] == False for post in post_results),
            "Not all posts returned are inactive",
        )

    def test_list_post_filter_by_published_date_today(self):
        url = reverse("post-list")
        today = timezone.now().strftime("%Y-%m-%d")
        response = self.client.get(
            url, {"published_date_start": today, "published_date_end": today}
        )
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_post_filter_by_published_date_today ======================"
        )
        print(f"Posts published today ({today}):")
        print(post_results)
        print(
            "====================== end test_list_post_filter_by_published_date_today ======================"
        )

        # assert that all post results is published today
        self.assertTrue(
            all(
                post["published_date"].startswith(timezone.now().strftime("%Y-%m-%d"))
                for post in post_results
            ),
            "Not all posts returned are published today",
        )

    def test_list_post_filter_by_published_date_yesterday(self):
        url = reverse("post-list")
        yesterday = (timezone.now() - timezone.timedelta(days=1)).strftime("%Y-%m-%d")
        response = self.client.get(
            url, {"published_date_start": yesterday, "published_date_end": yesterday}
        )
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_post_filter_by_published_date_yesterday ======================"
        )
        print(f"Posts published yesterday ({yesterday}):")
        print(post_results)
        print(
            "====================== end test_list_post_filter_by_published_date_yesterday ======================"
        )

        # assert that all post results is published yesterday
        self.assertTrue(
            all(post["published_date"].startswith(yesterday) for post in post_results),
            "Not all posts returned are published yesterday",
        )
