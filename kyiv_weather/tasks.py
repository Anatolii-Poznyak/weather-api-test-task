from celery import shared_task
from .scraper import sync_weather
from kyiv_weather.models import Weather


@shared_task
def my_task_weather():
    sync_weather()
