from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Author, Comment
from django.utils import timezone


class PostListEndpointTests(APITestCase):
    def setUp(self):
        # Create test user and author
        self.test_user = User.objects.create_user(
            username="testuser", email="test_user@example.com", password="testpassword"
        )
        self.test_author = Author.objects.create(
            name="Test Author", email="test_user@example.com", user=self.test_user
        )

        self.another_test_user = User.objects.create_user(
            username="anothertestuser",
            email="another_test_user@example.com",
            password="testpassword",
        )
        self.another_test_author = Author.objects.create(
            name="Test Author",
            email="another_test_user@example.com",
            user=self.test_user,
        )

        # Create test post dated today
        Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.another_test_author,
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
            author=self.another_test_author,
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

    def test_list_post_filter_by_published_date_2_weeks_ago(self):
        url = reverse("post-list")
        two_weeks_ago = (timezone.now() - timezone.timedelta(weeks=2)).strftime(
            "%Y-%m-%d"
        )
        response = self.client.get(
            url,
            {
                "published_date_start": two_weeks_ago,
                "published_date_end": two_weeks_ago,
            },
        )
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_post_filter_by_published_date_2_weeks_ago ======================"
        )
        print(f"Posts published 2 weeks ago ({two_weeks_ago}):")
        print(post_results)
        print(
            "====================== end test_list_post_filter_by_published_date_2_weeks_ago ======================"
        )

        # assert that all post results is published 2 weeks ago
        self.assertTrue(
            all(
                post["published_date"].startswith(two_weeks_ago)
                for post in post_results
            ),
            "Not all posts returned are published 2 weeks ago",
        )

    def test_list_post_filter_by_author(self):
        """Test filtering posts by author name. (case insensitive and partial match)"""
        url = reverse("post-list")
        search_string = "Test Auth"
        response = self.client.get(url, {"author_name": search_string})
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_post_filter_by_author ======================"
        )
        print(f"Posts by author {search_string}:")
        print(post_results)
        print(
            "====================== end test_list_post_filter_by_author ======================"
        )

        # assert that all post results is by the specified author
        self.assertTrue(
            all(search_string in post["author_name"] for post in post_results),
            "Not all posts returned are by the specified author",
        )

    def test_list_post_filter_by_title(self):
        """Test filtering posts by title. (case insensitive and partial match)"""
        url = reverse("post-list")
        search_string = "Test Post"
        response = self.client.get(url, {"title": search_string})
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_post_filter_by_title ======================"
        )
        print(f"Posts with title {search_string}:")
        print(post_results)
        print(
            "====================== end test_list_post_filter_by_title ======================"
        )

        # assert that all post results is by the specified author
        self.assertTrue(
            all(search_string in post["title"] for post in post_results),
            "Not all posts returned are by the specified author",
        )

    def test_list_post_filter_by_content(self):
        """Test filtering posts by content. (case insensitive and partial match)"""
        url = reverse("post-list")
        search_string = "Test content"
        response = self.client.get(url, {"content": search_string})
        self.assertEqual(response.status_code, 200)
        post_results = response.data.get("results", [])

        print(
            "====================== test_list_post_filter_by_content ======================"
        )
        print(f"Posts with content {search_string}:")
        print(post_results)
        print(
            "====================== end test_list_post_filter_by_content ======================"
        )

        # assert that all post results is by the specified author
        self.assertTrue(
            all(search_string in post["content"] for post in post_results),
            "Not all posts returned are by the specified author",
        )


class PostCreateUpdateDeleteEndpointTests(APITestCase):
    def setUp(self):
        # Create test user and author
        self.test_user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.test_author = Author.objects.create(
            name="Test Author", email="testuser@example.com", user=self.test_user
        )

        self.client.login(username="testuser", password="testpassword")
        self.auth_url = reverse("login")
        response = self.client.post(
            self.auth_url,
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.access_token = response.data.get("accessToken")
        self.refresh_token = response.data.get("refreshToken")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.url = reverse("post-list")
        self.valid_data = {
            "title": "New Post",
            "content": "This is a new post content.",
            "status": "published",
            "active": True,
        }

    def test_create_post_with_valid_data(self):
        """Test creating a post with valid data."""
        response = self.client.post(self.url, self.valid_data, format="json")
        print(
            "====================== test_create_post_with_valid_data ======================"
        )
        print(response.data)
        print(
            "====================== end test_create_post_with_valid_data ======================"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, "New Post")
        self.assertEqual(post.content, "This is a new post content.")
        self.assertEqual(post.author, self.test_author)
        self.assertEqual(post.status, "published")
        self.assertTrue(post.active)

    def test_edit_post_with_valid_data(self):
        """Test editing a post with valid data."""
        post = Post.objects.create(
            title="Old Post",
            content="This is an old post content.",
            author=self.test_author,
            status="draft",
            active=True,
        )
        edit_url = reverse("post-detail", args=[post.id])
        response = self.client.put(edit_url, self.valid_data, format="json")
        print(
            "====================== test_edit_post_with_valid_data ======================"
        )
        print(response.data)
        print(
            "====================== end test_edit_post_with_valid_data ======================"
        )
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.title, "New Post")
        self.assertEqual(post.content, "This is a new post content.")
        self.assertEqual(post.status, "published")
        self.assertTrue(post.active)

    def test_delete_post_as_author(self):
        """Test deleting a post."""
        post = Post.objects.create(
            title="Post to be deleted",
            content="This post will be deleted.",
            author=self.test_author,
            status="draft",
            active=True,
        )
        delete_url = reverse("post-detail", args=[post.id])
        response = self.client.delete(delete_url)
        print("====================== test_delete_post ======================")
        print(response.data)
        print("====================== end test_delete_post ======================")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), 0)


class CommentCreateEndpointTests(APITestCase):
    def setUp(self):
        # Create test user and author
        self.test_user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.test_author = Author.objects.create(
            name="Test Author", email="testuser@example.com", user=self.test_user
        )
        self.auth_url = reverse("login")

        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.test_author,
            status="published",
            active=True,
        )

    def login_user(self, user: User):
        """Helper method to log in a user."""
        self.client.login(username=user.username, password="testpassword")
        response = self.client.post(
            self.auth_url,
            {"username": user.username, "password": "testpassword"},
            format="json",
        )
        self.access_token = response.data.get("accessToken")
        self.refresh_token = response.data.get("refreshToken")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def logout_user(self):
        """Helper method to log out a user."""
        self.client.credentials(HTTP_AUTHORIZATION="")

    def test_create_comment_as_authenticated_user(self):
        """Test creating multimple comment as an authenticated user."""
        self.login_user(self.test_user)
        url = reverse("add_comment", args=[self.post.id])
        print(
            "====================== test_create_comment_as_authenticated_user ======================"
        )
        # 1
        response = self.client.post(
            url, {"content": "This is my first test comment."}, format="json"
        )
        print(1, response.data)
        # 2
        response = self.client.post(
            url, {"content": "This is my second test comment."}, format="json"
        )
        print(2, response.data)
        # 3
        response = self.client.post(
            url, {"content": "This is my last test comment."}, format="json"
        )
        print(3, response.data)
        print(
            "====================== end test_create_comment_as_authenticated_user ======================"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.filter(post=self.post).count(), 3)

    def test_create_comment_as_anonymous_user(self):
        """Test creating a comment as an anonymous user."""
        self.logout_user()
        url = reverse("add_comment", args=[self.post.id])
        print(
            "====================== test_create_comment_as_anonymous_user ======================"
        )
        response = self.client.post(
            url, {"content": "This is a test comment as anonymous user."}, format="json"
        )
        print(response.data)
        print(
            "====================== end test_create_comment_as_anonymous_user ======================"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.filter(post=self.post).count(), 1)
