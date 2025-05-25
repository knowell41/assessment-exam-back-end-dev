from django.contrib import admin
from .models import Author, Post, Comment


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "user")
    search_fields = ("name", "email")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "published_date", "status", "active")
    list_filter = ("status", "active", "published_date")
    search_fields = ("title", "content")
    date_hierarchy = "published_date"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created")
    list_filter = ("created",)
    search_fields = ("content",)
