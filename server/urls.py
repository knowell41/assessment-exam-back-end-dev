"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from server.api import HealthCheckView, LandingPageView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from server.auth import api as auth_api

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API documentation for the server project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # swagger documentation
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # lanidng page
    path("", LandingPageView.as_view(), name="landing_page"),
    # Add your app URLs here
    path("api/health-check/", HealthCheckView.as_view(), name="health_check"),
    # auth endponts
    path("api/auth/login/", auth_api.Login.as_view(), name="login"),
    path("api/auth/logout/", auth_api.Logout.as_view(), name="logout"),
    path("api/auth/verify/", auth_api.VerifyToken.as_view(), name="verify_token"),
    path(
        "api/auth/refresh/", auth_api.RefreshTokenView.as_view(), name="refresh_token"
    ),
]
