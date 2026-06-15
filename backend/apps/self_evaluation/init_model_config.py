from apps.self_evaluation.models import ModelConfig, FeatureModelAssignment

# Create ModelConfigs
deepseek = ModelConfig.objects.create(
    name="deepseek-chat",
    provider="deepseek",
    base_url="https://api.deepseek.com",
    temperature=0.5,
    active=True
)

openai = ModelConfig.objects.create(
    name="gpt-4o",
    provider="openai",
    base_url="",
    temperature=0.7,
    active=True
)

# Create Feature Assignments
FeatureModelAssignment.objects.create(
    feature_key="phq9",
    model=deepseek
)

FeatureModelAssignment.objects.create(
    feature_key="sdq",
    model=openai
)

FeatureModelAssignment.objects.create(
    feature_key="gad7",
    model=openai
)

print(" Initial models and feature assignments inserted.")
