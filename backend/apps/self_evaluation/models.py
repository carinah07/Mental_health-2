from django.db import models

class ChildAssessment(models.Model):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        
    ]

    assessment_type = models.CharField(max_length=10)
    age_group = models.CharField(max_length=10)  # (4-7, 8-12, 13-17) 
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    difficulties = models.PositiveIntegerField()
    prosocial = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    
    # Contact info to be filled later via follow-up form
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment #{self.id} - Score: {self.score}"
    
class SelfAssessment(models.Model):
    
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        
    ]

    assessment_type = models.CharField(max_length=10) #e.g phq9, gad7
    age_group = models.CharField(max_length=10)  # (12–15 , 16–20, 21–25 , 26–30, 31–40,40+) 
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    score = models.PositiveIntegerField()
    
    # Contact info to be filled later via follow-up form
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment #{self.id} - Score: {self.score}"

from django.db import models

class ModelConfig(models.Model):
    name = models.CharField(max_length=50)  # e.g., "deepseek-chat", "gpt-4"
    provider = models.CharField(max_length=20, choices=[
        ("openai", "OpenAI"),
        ("deepseek", "DeepSeek")
    ])
    base_url = models.URLField(blank=True, null=True)  # Optional for OpenAI
    temperature = models.FloatField(default=0.5)
    active = models.BooleanField(default=True)  # Optional filter

    def __str__(self):
        return f"{self.name} ({self.provider})"

class FeatureModelAssignment(models.Model):
    feature_key = models.CharField(max_length=50, unique=True, help_text="e.g. phq9, gad7, chatbot")
    model = models.ForeignKey(ModelConfig, on_delete=models.SET_NULL, null=True, related_name='assignments')

    def __str__(self):
        return f"{self.feature_key} → {self.model}"

