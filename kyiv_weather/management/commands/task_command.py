from django.core.management.base import BaseCommand
from kyiv_weather.tasks import main_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        main_task()
