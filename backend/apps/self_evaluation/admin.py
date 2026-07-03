from django.contrib import admin
from .models import SelfAssessment, ChildAssessment, ModelConfig, FeatureModelAssignment

@admin.register(SelfAssessment)
class SelfAssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "assessment_type", "score", "severity_level", "created_at")
    list_filter = ("assessment_type", "severity_level", "created_at")
    search_fields = ("user__username", "user__email")

@admin.register(ChildAssessment)
class ChildAssessmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "assessment_type", "score", "severity_level", "created_at")
    list_filter = ("assessment_type", "severity_level", "created_at")
    search_fields = ("user__username",)

@admin.register(ModelConfig)
class ModelConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "active", "temperature")
    list_filter = ("provider", "active")

@admin.register(FeatureModelAssignment)
class FeatureModelAssignmentAdmin(admin.ModelAdmin):
    list_display = ("feature_key", "model")
