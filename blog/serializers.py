from rest_framework import serializers
from .models import Author, Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "email", "user"]


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "published_date",
            "status",
            "active",
        ]
        read_only_fields = ["id", "published_date", "author"]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "author", "status", "active"]
        read_only_fields = ["author"]

    def validate(self, attrs):
        request = self.context.get("request")

        if request and request.method in ["PUT", "PATCH", "DELETE"]:
            post = self.instance
            print(f"Post instance: {post}")
            if post and post.author.user != request.user:
                raise serializers.ValidationError(
                    "You are not allowed to modify or delete a post that you do not own."
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "user", "content", "created"]
