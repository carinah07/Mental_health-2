import random
from datetime import timedelta

from django.utils import timezone

from apps.self_evaluation.models import SelfAssessment


def run():
    sexes = ["Male", "Female"]
    age_groups = ["12-15", "16-20", "21-25", "26-30", "31-40", "40+"]
    assessments = []

    for _ in range(200):
        assessment_type = random.choice(["phq9", "gad7"])
        score_max = 21 if assessment_type == "gad7" else 27

        assessments.append(
            SelfAssessment(
                assessment_type=assessment_type,
                age_group=random.choice(age_groups),
                sex=random.choice(sexes),
                score=random.randint(0, score_max),
                contact_info="0626231330",
                location=random.choice(["Dar es Salaam", "Dodoma", "Arusha", "Mbeya", "Mwanza"]),
                description=random.choice(["", "Reported fatigue and low mood.", "Follow-up recommended."]),
                created_at=timezone.now() - timedelta(days=random.randint(0, 60)),
            )
        )

    SelfAssessment.objects.bulk_create(assessments)
    print(f"Inserted {len(assessments)} synthetic assessments successfully.")
