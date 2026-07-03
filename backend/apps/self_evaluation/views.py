from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.http import FileResponse
import langdetect
from dotenv import load_dotenv

from apps.accounts.permissions import IsAdminUser
from .models import SelfAssessment, ChildAssessment, FeatureModelAssignment
from .prompts import generate_assessment_prompt
from .reports import severity_label, build_assessment_report, ASSESSMENT_LABELS
from common.ai_clients import get_model_client_for_feature

User = get_user_model()

load_dotenv()


def _collect_reports_for_user(user):
    reports = []
    self_items = SelfAssessment.objects.filter(user=user).order_by("-created_at")
    child_items = ChildAssessment.objects.filter(user=user).order_by("-created_at")

    for item in self_items:
        label, max_score = ASSESSMENT_LABELS.get(item.assessment_type, (item.assessment_type, item.score))
        reports.append(
            {
                "id": item.id,
                "type": "self",
                "assessment_type": item.assessment_type,
                "title": label,
                "score": item.score,
                "max_score": max_score,
                "severity": item.severity_level,
                "created_at": item.created_at.isoformat(),
            }
        )
    for item in child_items:
        label, max_score = ASSESSMENT_LABELS.get(item.assessment_type, (item.assessment_type, item.score))
        reports.append(
            {
                "id": item.id,
                "type": "child",
                "assessment_type": item.assessment_type,
                "title": label,
                "score": item.score,
                "max_score": max_score,
                "severity": item.severity_level,
                "created_at": item.created_at.isoformat(),
            }
        )

    reports.sort(key=lambda r: r["created_at"], reverse=True)
    return reports


def _get_assessment_record(user, report_type, pk):
    if report_type == "child":
        record = ChildAssessment.objects.get(pk=pk, user=user)
        return record, "child"
    record = SelfAssessment.objects.get(pk=pk, user=user)
    return record, "self"


def _run_assessment(request, assessment_type, expected_count, max_score, feature_key, is_child=False):
    scores = request.data.get("scores", [])
    responses = request.data.get("responses", [])
    lang_text = request.data.get("lang_text")
    user_type = request.data.get("user_type")
    age_group = request.data.get("age_group")
    sex = request.data.get("sex")

    questions = [r.get("question") for r in responses]

    if not scores or not questions or len(scores) != expected_count or len(questions) != expected_count:
        return Response(
            {"error": f"Invalid or incomplete {assessment_type.upper()} input."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    total_score = sum(scores)
    lang = langdetect.detect(lang_text)
    severity = severity_label(assessment_type, total_score)

    if is_child:
        difficulties = request.data.get("difficulties")
        prosocial = request.data.get("prosocial")
        record = ChildAssessment.objects.create(
            user=request.user,
            assessment_type=assessment_type,
            age_group=age_group,
            sex=sex,
            difficulties=difficulties,
            prosocial=prosocial,
            score=total_score,
            severity_level=severity,
        )
        prompt = generate_assessment_prompt(
            user_type, total_score, max_score, age_group, lang, zip(questions, scores), is_child=True
        )
        redirect_link = f"/followup/child/{record.id}" if total_score >= 19 else None
        report_type = "child"
    else:
        record = SelfAssessment.objects.create(
            user=request.user,
            assessment_type=assessment_type,
            age_group=age_group,
            sex=sex,
            score=total_score,
            severity_level=severity,
        )
        prompt = generate_assessment_prompt(
            user_type, total_score, max_score, age_group, lang, zip(questions, scores)
        )
        redirect_link = f"/followup/{record.id}" if total_score >= 19 else None
        report_type = "self"

    client, model_name, temperature = get_model_client_for_feature(feature_key, FeatureModelAssignment)
    chat_response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        stream=False,
    )

    result = chat_response.choices[0].message.content.strip()
    record.ai_response = result
    record.save(update_fields=["ai_response"])

    return Response(
        {
            "assessment_id": record.id,
            "assessment_type": assessment_type,
            "report_type": report_type,
            "score": total_score,
            "severity": severity,
            "response": result,
            "redirect_link": redirect_link,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def phq9_assessment(request):
    try:
        return _run_assessment(request, "phq9", 9, 27, "phq9")
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def gad7_assessment(request):
    try:
        return _run_assessment(request, "gad7", 7, 21, "gad7")
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def child_assessment(request):
    try:
        scores = request.data.get("scores", [])
        if len(scores) != 25:
            return Response({"error": "Invalid or incomplete SDQ input."}, status=status.HTTP_400_BAD_REQUEST)
        return _run_assessment(request, "sdq", 25, 50, "sdq", is_child=True)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_reports(request):
    return Response(_collect_reports_for_user(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_report(request, report_type, pk):
    try:
        record, kind = _get_assessment_record(request.user, report_type, pk)
    except (SelfAssessment.DoesNotExist, ChildAssessment.DoesNotExist):
        return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

    buffer = build_assessment_report(request.user, record, assessment_kind=kind)
    filename = f"mindcare-report-{record.assessment_type}-{record.id}.docx"
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=filename,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_user_reports(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
        },
        "reports": _collect_reports_for_user(user),
    })


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_download_user_report(request, user_id, report_type, pk):
    try:
        user = User.objects.get(pk=user_id)
        record, kind = _get_assessment_record(user, report_type, pk)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except (SelfAssessment.DoesNotExist, ChildAssessment.DoesNotExist):
        return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

    buffer = build_assessment_report(user, record, assessment_kind=kind)
    filename = f"mindcare-report-{user.username}-{record.assessment_type}-{record.id}.docx"
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=filename,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_followup_details(request, pk):
    try:
        assessment = SelfAssessment.objects.get(pk=pk, user=request.user)

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
@permission_classes([IsAuthenticated])
def update_followup_details_child(request, pk):
    try:
        assessment = ChildAssessment.objects.get(pk=pk, user=request.user)

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
