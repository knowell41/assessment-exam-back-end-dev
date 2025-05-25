from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from blog.serializers import (
    AuthorSerializer,
    PostSerializer,
    CommentSerializer,
    PostCreateSerializer,
)
from blog.models import Author, Post, Comment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Post instances.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="List all posts",
        operation_description="Retrieve a list of all posts in the system.",
        responses={
            200: PostSerializer(many=True),
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
        ],
    )
    def list(self, request, *args, **kwargs):
        page_size = request.query_params.get("page_size")
        if page_size:
            self.paginator.page_size = int(page_size)
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a post by ID",
        operation_description="Retrieve a single post by its ID.",
        responses={
            200: PostSerializer,
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
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new post",
        operation_description="Create a new post with the provided data.",
        request_body=PostCreateSerializer,
        responses={
            201: PostSerializer,
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
            200: PostSerializer,
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
        return Response(PostSerializer(instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Partially update a post",
        operation_description="Partially update a post with the provided data.",
        request_body=PostSerializer,
        responses={
            200: PostSerializer,
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
