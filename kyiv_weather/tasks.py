from celery import shared_task
from kyiv_weather.scraper import sync_weather
from django_celery_beat.models import PeriodicTask, CrontabSchedule


@shared_task(bind=True)
def update_weather(self):
    sync_weather()
    return self.request.id


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

    task_name = "Weather daily update"

    periodic_task, created = PeriodicTask.objects.get_or_create(
        name=task_name,
        defaults={
            "crontab": schedule,
            "task": "kyiv_weather.tasks.my_task_weather",
            "args": "[]"
        },
    )

    if not created:
        periodic_task.crontab = schedule
        periodic_task.save()