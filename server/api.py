from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from django.shortcuts import render


class LandingPageView(APIView):
    """
    A simple landing page with 2 buttons:
    - One to view the API documentation
    - One to view the blog
    """

    @swagger_auto_schema(
        operation_description="Landing page with buttons to view API documentation and blog",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Landing page message",
                    )
                },
            )
        },
        tags=["Landing Page"],
    )
    def get(self, request):
        """
        Renders the landing page using the landingPage.html template.
        """
        return render(request, "landingPage.html")


class HealthCheckView(APIView):
    """
    A simple health check endpoint to verify that the server is running.
    """

    @swagger_auto_schema(
        operation_description="Check the health of the server",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Health status of the server",
                    )
                },
            )
        },
        tags=["Health Check"],
    )
    def get(self, request):
        """
        Returns a 200 OK response to indicate that the server is healthy.
        """
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
