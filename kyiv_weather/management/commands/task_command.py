from django.core.management.base import BaseCommand
from kyiv_weather.tasks import main_task


class Command(BaseCommand):
    help = "Runs the main task with 9 hour by default, or specific hour if argument is passed"

    def add_arguments(self, parser):
        parser.add_argument(
            "hour",
            nargs="?",
            type=str,
            help="The hour in '24format' when the task should run",
            default="9"
        )

    def handle(self, *args, **options):
        hour = options.get("hour", "9")
        main_task(hour=hour)
