from django.core.management.base import BaseCommand
from staff_module.models import CustomUser, Site, Language, Floor
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Creates a new superuser"

    def handle(self, *args, **kwargs):
        try:
            site = Site.objects.get(code="szz")
        except Site.DoesNotExist:
            site = Site.objects.create(code="szz")
            self.stdout.write(self.style.SUCCESS("Created new Site"))

        try:
            language = Language.objects.get(code="eng")
        except Language.DoesNotExist:
            language = Language.objects.create(code="eng")
            self.stdout.write(self.style.SUCCESS("Created new Language"))

        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")

        try:
            user = CustomUser.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                site=site,
                language=language,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created superuser {username}")
            )
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"Error creating superuser: {e}"))
