from celery import shared_task
from .scraper import sync_weather
from django_celery_beat.models import PeriodicTask, CrontabSchedule


@shared_task
def my_task_weather():
    sync_weather()


def main_task():
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="9",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
    )

    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name="Update weather daily",
        task="kyiv_weather.tasks.my_task_weather",
        args="[]",
    )
