from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(title="MindCare Mental Health API", default_version='v1'),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/chatbot/", include("apps.chatbot.urls")),
    path("api/assessment/", include("apps.self_evaluation.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
