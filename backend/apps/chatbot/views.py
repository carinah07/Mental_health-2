from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import os
import langdetect
from dotenv import load_dotenv

load_dotenv()

def get_deepseek_client():
    deepseek_key = os.getenv("DEEPSEEK_API_KEY2")
    if not deepseek_key:
        return None
    return OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")

# Mental health keywords for content filtering
MENTAL_HEALTH_KEYWORDS = [
    "stress", "depression", "anxiety", "lonely", "mental", "wellbeing", "panic",
    "trauma", "abuse", "grief", "therapy", "counseling", "self-harm", "burnout", "sad"
]

def is_mental_health_related(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in MENTAL_HEALTH_KEYWORDS)

@api_view(["POST"])
def akili_chat(request):
    try:
        # Validate input
        user_input = request.data.get("message", "")
        history = request.data.get("history", [])[-10:]  # Keep last 10 messages
        
        if not user_input:
            return Response({"error": "No message provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Detect user language
        try:
            lang = langdetect.detect(user_input)
        except Exception:
            lang = "en"  # Default to English if detection fails

        # Build system prompt with all combined features
        system_prompt = (
            "You are Mia, a supportive and empathetic AI mental health assistant built for the MindCare platform. "
            "You specialize in psychological and emotional wellbeing support. "
            "Focus on helping users understand and manage their emotional and mental wellbeing.\n\n"
            "Guidelines:\n"
            "1. Respond only in the user's detected language\n"
            "2. Use markdown formatting (**bold**, *italic*, [links](https://...), > quotes)\n"
            "3. Keep greetings brief and without non-requested content\n"
            "4. For critical situations, encourage the user to seek professional help from a licensed mental health professional\n"
            "5. Gently decline non-mental-health questions with a supportive tone\n"
            "6. Provide practical coping strategies and emotional support\n"
            "7. Never offer medical diagnosis or treatment advice"
        )

        # Prepare message history
        messages = [{"role": "system", "content": system_prompt}]

        # Process history messages (handles both string and dict formats)
        for msg in history:
            if isinstance(msg, dict):
                role = "user" if msg.get("sender") == "user" else "assistant"
                content = msg.get("text", "")
            else:
                role = "user"  # Default for string format
                content = str(msg)
            
            if content.strip():  # Only add non-empty messages
                messages.append({"role": role, "content": content})

        # Add current message
        messages.append({"role": "user", "content": user_input})

        # Optional content filtering
        # if not is_mental_health_related(user_input):
        #     return Response({
        #         "response": "I specialize in emotional wellbeing discussions. "
        #         "How can I support you with psychological or emotional concerns today?"
        #     })

        # Make API call to DeepSeek
        client_deepseek = get_deepseek_client()
        if not client_deepseek:
            return Response(
                {"error": "Chat service is currently unavailable"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Try multiple possible model names
        model_names = ["deepseek-chat", "deepseek-v1", "deepseek-v2", "deepseek-llm"]
        last_error = None
        
        for model_name in model_names:
            try:
                response = client_deepseek.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.7
                )
                return Response({"response": response.choices[0].message.content})
            except Exception as e:
                last_error = e
                continue

        # If all model names failed
        return Response(
            {"error": f"Failed to get response: {str(last_error)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
