from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update the default MindCare admin account"

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin")
        parser.add_argument("--email", default="admin@mindcare.com")
        parser.add_argument("--password", default="Admin@123")
        parser.add_argument("--first-name", default="System Admin")

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]
        first_name = options["first_name"]

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = email
        user.first_name = first_name
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(
            f"{action} admin user '{username}' (password: {password})"
        ))
