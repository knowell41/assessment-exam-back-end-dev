from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from blog.serializers import (
    PostWithCommentsSerializer,
    PostCreateSerializer,
    PostMinimalSerializer,
    CommentSerializer,
)
from blog.models import Author, Post, Comment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)


class PostViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Post instances.
    """

    queryset = Post.objects.all()
    serializer_class = PostMinimalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="List all posts",
        operation_description="Retrieve a list of all posts in the system.",
        responses={
            200: PostMinimalSerializer(many=True),
            400: "Bad request.",
            500: "Internal server error.",
        },
        tags=["Posts"],
        manual_parameters=[
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of posts per page for pagination",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "active",
                openapi.IN_QUERY,
                description="Filter posts by active status",
                type=openapi.TYPE_BOOLEAN,
                required=False,
            ),
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                description="Filter posts by status (draft/published)",
                type=openapi.TYPE_STRING,
                enum=["draft", "published"],
                required=False,
            ),
            openapi.Parameter(
                "title",
                openapi.IN_QUERY,
                description="Filter posts by title (case-insensitive substring match)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "content",
                openapi.IN_QUERY,
                description="Filter posts by content (case-insensitive substring match)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "author_name",
                openapi.IN_QUERY,
                description="Filter posts by author's name (case-insensitive substring match)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        page_size = request.query_params.get("page_size")
        active_param = request.query_params.get("active")
        if active_param is not None:
            is_active = active_param == "true"
        else:
            is_active = True
        self.queryset = self.queryset.filter(active=is_active)
        title_param = request.query_params.get("title")
        if title_param:
            self.queryset = self.queryset.filter(title__icontains=title_param)
        content_param = request.query_params.get("content")
        if content_param:
            self.queryset = self.queryset.filter(content__icontains=content_param)
        author_name_param = request.query_params.get("author_name")
        if author_name_param:
            self.queryset = self.queryset.filter(
                author__name__icontains=author_name_param
            )
        if page_size:
            self.paginator.page_size = int(page_size)
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a post by ID",
        operation_description="Retrieve a single post by its ID.",
        responses={
            200: PostMinimalSerializer,
            404: "Not found.",
            500: "Internal server error.",
        },
        tags=["Posts"],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single post by ID.
        """
        instance = self.get_object()
        serializer = PostWithCommentsSerializer(instance, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new post",
        operation_description="Create a new post with the provided data.",
        request_body=PostCreateSerializer,
        responses={
            201: PostMinimalSerializer,
            400: "Bad request.",
            500: "Internal server error.",
        },
        tags=["Posts"],
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new post.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author = Author.objects.filter(user=request.user).first()
        if not author:
            new_author = Author.objects.create(
                name=request.user.username, email=request.user.email, user=request.user
            )
        serializer.save(author=author or new_author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Update an existing post",
        operation_description="Update an existing post with the provided data.",
        request_body=PostCreateSerializer,
        responses={
            200: PostMinimalSerializer,
            400: "Bad request.",
            404: "Not found.",
            500: "Internal server error.",
        },
        tags=["Posts"],
    )
    def update(self, request, *args, **kwargs):
        """
        Update an existing post.
        """
        instance = self.get_object()
        serializer = PostCreateSerializer(
            instance, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(PostMinimalSerializer(instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Partially update a post",
        operation_description="Partially update a post with the provided data.",
        request_body=PostCreateSerializer,
        responses={
            200: PostMinimalSerializer,
            400: "Bad request.",
            404: "Not found.",
            500: "Internal server error.",
        },
        tags=["Posts"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a post",
        operation_description="Delete a post by its ID.",
        responses={
            204: "No content.",
            404: "Not found.",
            500: "Internal server error.",
        },
        tags=["Posts"],
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a post.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddCommentAPIView(APIView):
    """
    A view to add a comment to a post.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Add a comment to a post",
        operation_description="Add a comment to a post by providing the post ID and comment content.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "content": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Comment content"
                ),
            },
            required=["content"],
        ),
        responses={
            201: openapi.Response("Comment created successfully"),
            400: "Bad request.",
            404: "Post not found.",
            500: "Internal server error.",
        },
        tags=["Comments"],
    )
    def post(self, request, **kwargs):
        """
        Add a comment to a post.
        """
        post_id = kwargs.get("post_id")
        content = request.data.get("content")

        if not content:
            return Response(
                {"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        data = {"post": post, "content": content}
        if request.user and request.user.is_authenticated:
            data["user"] = request.user

        new_comment = Comment.objects.create(**data)
        serializer = CommentSerializer(new_comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveCommentAPIView(APIView):
    """
    A view to remove a comment from a post.
    Only the author of the comment or the post can delete the comment.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Remove a comment from a post",
        operation_description="Remove a comment from a post by providing the post ID and comment ID.",
        responses={
            204: "Comment deleted successfully",
            404: "Post or comment not found.",
            500: "Internal server error.",
        },
        tags=["Comments"],
    )
    def delete(self, request, **kwargs):
        """
        Remove a comment from a post.
        """
        post_id = kwargs.get("post_id")
        comment_id = kwargs.get("comment_id")

        try:
            post = Post.objects.get(id=post_id)
            comment = Comment.objects.get(id=comment_id, post=post)
        except (Post.DoesNotExist, Comment.DoesNotExist):
            return Response(
                {"error": "Post or comment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if self.validate(post, comment) is False:
            return Response(
                {"error": "You are not allowed to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def validate(self, post: Post, comment: Comment) -> bool:
        """
        Validate if the user is allowed to delete the comment.
        Only the author of the comment or the post can delete the comment.
        """
        if comment.user == self.request.user or post.author.user == self.request.user:
            return True
        return False
