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


class PostMinimalSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "published_date", "author_name"]

    def get_author_name(self, obj):
        return obj.author.name if obj.author else "Unknown Author"


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "author", "status", "active"]
        read_only_fields = ["author"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "PATCH":
            for field in self.fields.values():
                field.required = False

    def validate(self, attrs):
        request = self.context.get("request")

        if request and request.method in ["PUT", "PATCH", "DELETE"]:
            post = self.instance
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
