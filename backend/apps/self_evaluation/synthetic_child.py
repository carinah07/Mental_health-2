import random
from datetime import timedelta

from django.utils import timezone

from apps.self_evaluation.models import ChildAssessment


def run():
    sexes = ["Male", "Female"]
    age_groups = ["4-7", "8-12", "13-17"]
    assessments = []

    for _ in range(200):
        difficulties = random.randint(0, 50)
        prosocial = random.randint(0, 10)

        assessments.append(
            ChildAssessment(
                assessment_type="sdq",
                age_group=random.choice(age_groups),
                sex=random.choice(sexes),
                difficulties=difficulties,
                prosocial=prosocial,
                score=difficulties + prosocial,
                contact_info="0626231330",
                location=random.choice(["Dar es Salaam", "Dodoma", "Arusha", "Mbeya", "Mwanza"]),
                description="",
                school="",
                created_at=timezone.now() - timedelta(days=random.randint(0, 60)),
            )
        )

    ChildAssessment.objects.bulk_create(assessments)
    print(f"Inserted {len(assessments)} synthetic assessments successfully.")
