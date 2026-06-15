import os

from openai import OpenAI


def get_model_client_for_feature(feature_key, assignment_model):
    assignment = assignment_model.objects.select_related("model").filter(feature_key=feature_key).first()
    if not assignment or not assignment.model:
        raise Exception(f"No model assigned for feature '{feature_key}'")

    model = assignment.model
    if model.provider == "deepseek":
        client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY2"), base_url=model.base_url or "https://api.deepseek.com")
    elif model.provider == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY2"))
    else:
        raise Exception(f"Unsupported provider: {model.provider}")

    return client, model.name, model.temperature
