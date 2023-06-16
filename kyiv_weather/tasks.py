from celery import shared_task
from .scraper import sync_weather
from django_celery_beat.models import PeriodicTask, CrontabSchedule


def main_task(
        minute="0",
        hour="9",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
):
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=minute,
        hour=hour,
        day_of_week=day_of_week,
        day_of_month=day_of_month,
        month_of_year=month_of_year
    )

    PeriodicTask.objects.update_or_create(
        crontab=schedule,
        name="Weather daily update",
        defaults={
            "task": "kyiv_weather.tasks.my_task_weather",
            "args": "[]"
        },
    )
