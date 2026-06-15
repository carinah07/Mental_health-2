from django.core.management.base import BaseCommand
from apps.self_evaluation.models import SelfAssessment

class Command(BaseCommand):
    help = 'Clears all records from SelfAssessment'

    def handle(self, *args, **kwargs):
        deleted_count, _ = SelfAssessment.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'{deleted_count} records deleted from SelfAssessment'))
