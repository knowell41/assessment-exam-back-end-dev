from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.api import PostViewSet, AddCommentAPIView, RemoveCommentAPIView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    # comment
    path(
        "posts/<int:post_id>/comments/", AddCommentAPIView.as_view(), name="add_comment"
    ),
    path(
        "posts/<int:post_id>/comments/<int:comment_id>/",
        RemoveCommentAPIView.as_view(),
        name="delete_comment",
    ),
]
