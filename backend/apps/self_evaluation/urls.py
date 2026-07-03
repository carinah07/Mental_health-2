from django.urls import path
from .views import (
    phq9_assessment,
    gad7_assessment,
    child_assessment,
    update_followup_details,
    update_followup_details_child,
    list_reports,
    download_report,
    admin_list_user_reports,
    admin_download_user_report,
)

urlpatterns = [
    path("phq9/", phq9_assessment, name="phq9"),
    path("gad7/", gad7_assessment, name="gad7"),
    path("sdq/", child_assessment, name="sdq"),
    path("reports/", list_reports, name="list_reports"),
    path("reports/<str:report_type>/<int:pk>/download/", download_report, name="download_report"),
    path("admin/users/<int:user_id>/reports/", admin_list_user_reports, name="admin_list_user_reports"),
    path(
        "admin/users/<int:user_id>/reports/<str:report_type>/<int:pk>/download/",
        admin_download_user_report,
        name="admin_download_user_report",
    ),
    path("followup/<int:pk>/", update_followup_details, name="update_followup"),
    path("followup/child/<int:pk>/", update_followup_details_child, name="update_followup_child"),
]
