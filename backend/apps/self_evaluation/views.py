from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import langdetect
from dotenv import load_dotenv
from .models import SelfAssessment, ChildAssessment, FeatureModelAssignment
from .prompts import generate_assessment_prompt
from common.ai_clients import get_model_client_for_feature

load_dotenv()

@api_view(["POST"])
def phq9_assessment(request):
    try:
        scores = request.data.get("scores", [])
        responses = request.data.get("responses", [])
        lang_text = request.data.get("lang_text")
        user_type = request.data.get("user_type")
        age_group = request.data.get("age_group")
        sex = request.data.get("sex")

        questions = [r.get("question") for r in responses]

        if not scores or not questions or len(scores) != 9 or len(questions) != 9:
            return Response({"error": "Invalid or incomplete PHQ-9 input."}, status=status.HTTP_400_BAD_REQUEST)

        total_score = sum(scores)
        lang = langdetect.detect(lang_text)

        record = SelfAssessment.objects.create(
            assessment_type = 'phq9',
            age_group=age_group,
            sex=sex,
            score=total_score
        )

        prompt = generate_assessment_prompt(user_type, total_score, 27, age_group, lang, zip(questions, scores))

        client, model_name, temperature = get_model_client_for_feature("phq9", FeatureModelAssignment)
        chat_response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=False
        )

        result = chat_response.choices[0].message.content.strip()
        redirect_link = f"/followup/{record.id}" if total_score >= 19 else None

        return Response({
            "score": total_score,
            "response": result,
            "redirect_link": redirect_link
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def gad7_assessment(request):
    try:
        scores = request.data.get("scores", [])
        responses = request.data.get("responses", [])
        lang_text = request.data.get("lang_text")
        user_type = request.data.get("user_type")
        age_group = request.data.get("age_group")
        sex = request.data.get("sex")

        questions = [r.get("question") for r in responses]

        if not scores or not questions or len(scores) != 7 or len(questions) != 7:
            return Response({"error": "Invalid or incomplete GAD-7 input."}, status=status.HTTP_400_BAD_REQUEST)

        total_score = sum(scores)
        lang = langdetect.detect(lang_text)
        record = SelfAssessment.objects.create(assessment_type = 'gad7', age_group=age_group, sex=sex, score=total_score)

        prompt = generate_assessment_prompt(user_type, total_score, 21, age_group, lang, zip(questions, scores))

        client, model_name, temperature = get_model_client_for_feature("gad7", FeatureModelAssignment)
        chat_response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=False
        )

        result = chat_response.choices[0].message.content.strip()
        redirect_link = f"/followup/{record.id}" if total_score >= 19 else None

        return Response({"score": total_score, "response": result, "redirect_link": redirect_link}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def child_assessment(request):
    try:
        scores = request.data.get("scores", [])
        responses = request.data.get("responses", [])
        lang_text = request.data.get("lang_text")
        user_type = request.data.get("user_type")
        difficulties = request.data.get("difficulties")
        prosocial = request.data.get("prosocial")
        age_group = request.data.get("age_group")
        sex = request.data.get("sex")

        questions = [r.get("question") for r in responses]

        if not scores or not questions or len(scores) != len(questions):
            return Response({"error": "Invalid or incomplete SDQ input."}, status=status.HTTP_400_BAD_REQUEST)

        total_score = sum(scores)
        lang = langdetect.detect(lang_text)
        record = ChildAssessment.objects.create( assessment_type = 'sdq',  age_group=age_group, sex=sex, difficulties=difficulties, prosocial=prosocial, score=total_score)

        prompt = generate_assessment_prompt(user_type, total_score, 50, age_group, lang, zip(questions, scores), is_child=True)

        client, model_name, temperature = get_model_client_for_feature("sdq", FeatureModelAssignment)
        chat_response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=False
        )

        result = chat_response.choices[0].message.content.strip()
        redirect_link = f"/followup/{record.id}" if total_score >= 19 else None

        return Response({"score": total_score, "response": result, "redirect_link": redirect_link}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
def update_followup_details(request, pk):
    try:
        assessment = SelfAssessment.objects.get(pk=pk)

        contact_info = request.data.get("contact_info")
        location = request.data.get("location")
        description = request.data.get("description")

        if not contact_info or not location:
            return Response({"error": "Contact info and location are required."}, status=status.HTTP_400_BAD_REQUEST)

        assessment.contact_info = contact_info
        assessment.location = location
        assessment.description = description
        assessment.save()

        return Response({"message": "Details updated successfully."}, status=status.HTTP_200_OK)

    except SelfAssessment.DoesNotExist:
        return Response({"error": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def update_followup_details_child(request, pk):
    try:
        assessment = ChildAssessment.objects.get(pk=pk)

        contact_info = request.data.get("contact_info")
        location = request.data.get("location")
        school = request.data.get("school")
        description = request.data.get("description")

        if not contact_info or not location:
            return Response({"error": "Contact info and location are required."}, status=status.HTTP_400_BAD_REQUEST)

        assessment.contact_info = contact_info
        assessment.location = location
        assessment.school = school
        assessment.description = description
        assessment.save()

        return Response({"message": "Details updated successfully."}, status=status.HTTP_200_OK)

    except ChildAssessment.DoesNotExist:
        return Response({"error": "Assessment not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

