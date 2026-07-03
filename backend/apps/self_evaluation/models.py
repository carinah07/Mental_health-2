from django.conf import settings
from django.db import models


class ChildAssessment(models.Model):
    SEX_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="child_assessments",
        null=True,
        blank=True,
    )
    assessment_type = models.CharField(max_length=10)
    age_group = models.CharField(max_length=10)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    difficulties = models.PositiveIntegerField()
    prosocial = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    ai_response = models.TextField(blank=True, default="")
    severity_level = models.CharField(max_length=30, blank=True, default="")

    contact_info = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Child Assessment #{self.id} - Score: {self.score}"


class SelfAssessment(models.Model):
    SEX_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="self_assessments",
        null=True,
        blank=True,
    )
    assessment_type = models.CharField(max_length=10)
    age_group = models.CharField(max_length=10)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    score = models.PositiveIntegerField()
    ai_response = models.TextField(blank=True, default="")
    severity_level = models.CharField(max_length=30, blank=True, default="")

    contact_info = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment #{self.id} - Score: {self.score}"


class ModelConfig(models.Model):
    name = models.CharField(max_length=50)
    provider = models.CharField(
        max_length=20,
        choices=[
            ("openai", "OpenAI"),
            ("deepseek", "DeepSeek"),
        ],
    )
    base_url = models.URLField(blank=True, null=True)
    temperature = models.FloatField(default=0.5)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.provider})"


class FeatureModelAssignment(models.Model):
    feature_key = models.CharField(
        max_length=50, unique=True, help_text="e.g. phq9, gad7, chatbot"
    )
    model = models.ForeignKey(
        ModelConfig, on_delete=models.SET_NULL, null=True, related_name="assignments"
    )

    def __str__(self):
        return f"{self.feature_key} → {self.model}"
