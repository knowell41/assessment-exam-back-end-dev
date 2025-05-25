from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from drf_yasg import openapi
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


class Login(APIView):
    """
    API endpoint for user login with username and password using JWT.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login with username and password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Username"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Password"
                ),
            },
            required=["username", "password"],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Success message"
                    ),
                    "token": openapi.Schema(
                        type=openapi.TYPE_STRING, description="JWT token"
                    ),
                },
            ),
            400: "Bad request.",
            401: "Unauthorized.",
            500: "Internal server error.",
        },
        tags=["Auth"],
        operation_description="This endpoint allows users to log in with their username and password and receive a JWT token.",
        operation_id="login",
    )
    def post(self, request):
        """
        Handle user login with username and password using JWT.
        """

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "accessToken": access_token,
                "refreshToken": str(refresh),
                "user": {
                    # "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )

    def get_dispenza_admin_user_info(self, email: str) -> dict:
        """
        Get Dispenza admin user information.
        """
        try:
            user = DispenzaUser.objects.using("dispenza-admin").filter(email=email)
            print("=========================")
            print(user)

        except User.DoesNotExist:
            return None


class VerifyToken(APIView):
    """
    API endpoint to verify JWT token.
    """

    @swagger_auto_schema(
        operation_summary="Verify JWT token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="JWT token"
                ),
            },
            required=["token"],
        ),
        responses={
            200: "Token is valid.",
            400: "Token is invalid.",
            401: "Unauthorized.",
            500: "Internal server error.",
        },
        tags=["Auth"],
        operation_description="This endpoint allows users to verify their JWT token.",
        operation_id="verify_token",
    )
    def post(self, request):
        """
        Handle token verification.
        """
        token = request.data.get("token")
        try:
            token_obj = AccessToken(token)
            if token_obj:
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )


class RefreshTokenView(APIView):
    """
    API endpoint to refresh JWT tokens.
    """

    @swagger_auto_schema(
        operation_summary="Refresh JWT token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refreshToken": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh token"
                ),
            },
            required=["refreshToken"],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "accessToken": openapi.Schema(
                        type=openapi.TYPE_STRING, description="New access token"
                    ),
                    "refreshToken": openapi.Schema(
                        type=openapi.TYPE_STRING, description="New refresh token"
                    ),
                },
            ),
            400: "Bad request.",
            401: "Unauthorized.",
            500: "Internal server error.",
        },
        tags=["Auth"],
        operation_description="This endpoint allows users to refresh their JWT tokens using a valid refresh token.",
        operation_id="refresh_token",
    )
    def post(self, request):
        """
        Handle token refresh.
        """
        refresh_token = request.data.get("refreshToken")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)

            return Response(
                {
                    "accessToken": new_access_token,
                    "refreshToken": new_refresh_token,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token", "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class Logout(APIView):
    """
    API endpoint to log out and blacklist the refresh token.
    """

    @swagger_auto_schema(
        operation_summary="Logout and blacklist refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refreshToken": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh token"
                ),
            },
            required=["refreshToken"],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Success message"
                    ),
                },
            ),
            400: "Bad request.",
            401: "Unauthorized.",
            500: "Internal server error.",
        },
        tags=["Auth"],
        operation_description="This endpoint allows users to log out by blacklisting their refresh token.",
        operation_id="logout",
    )
    def post(self, request):
        """
        Handle user logout and blacklist the refresh token.
        """
        refresh_token = request.data.get("refreshToken")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            # Blacklist the refresh token
            outstanding_token = OutstandingToken.objects.filter(
                jti=refresh["jti"]
            ).first()

            # Optionally, you can also delete the access token if needed
            BlacklistedToken.objects.create(token=outstanding_token)
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            return Response(
                {"error": "Invalid refresh token", "details": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )
