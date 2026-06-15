from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include


schema_view = get_schema_view(
   openapi.Info(title="MindCare Mental Health API", default_version='v1'),
   public=True,
)

urlpatterns = [
    path("api/chatbot/", include("apps.chatbot.urls")),
    path("api/assessment/", include("apps.self_evaluation.urls")),
    path("api/education/", include("apps.education.urls")),
    path("api/experts/", include("apps.experts.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
