import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=os.environ["ADMIN_USERNAME"]).exists():
            superuser = User.objects.create_superuser(
                username=os.environ["ADMIN_USERNAME"],
                password=os.environ["ADMIN_PASSWORD"],
            )
            print(f"\n\033[92m  Superuser {superuser.username} was created successfully!\033[0m")

        else:
            print(f"\033[91m  This superuser already exists!\033[0m")
