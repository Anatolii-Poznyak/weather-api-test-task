from datetime import timedelta

import cloudscraper
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from django.utils import timezone

from config.settings import KYIV_WEATHER_API_URL
from kyiv_weather.exceptions import NetworkError, ParsingError, DataExtractionError
from kyiv_weather.models import Weather


def parse_weather() -> list[Weather]:
    try:
        scraper = cloudscraper.create_scraper()
        page = scraper.get(KYIV_WEATHER_API_URL).content
    except RequestException:
        raise NetworkError()

    try:
        soup = BeautifulSoup(page, "html.parser")
        five_days = soup.select(".five-days__day.fl-col")
        start_date = timezone.now().date()
    except Exception:
        raise ParsingError()

    try:
        return [
            Weather(
                date=start_date + timedelta(days=index),
                temperature=int(day.select_one(".high").text.replace("°", "")),
                description=day.select_one(".five-days__icon")["data-tippy-content"],
            )
            for index, day in enumerate(five_days)
        ]
    except Exception:
        raise DataExtractionError()


def save_weather(five_days_weather: list[Weather]) -> None:
    for one_day_weather in five_days_weather:
        Weather.objects.update_or_create(
            date=one_day_weather.date,
            defaults={
                "temperature": one_day_weather.temperature,
                "description": one_day_weather.description,
            },
        )


def sync_weather() -> None:
    try:
        weather = parse_weather()
        save_weather(weather)
    except (NetworkError, ParsingError, DataExtractionError) as e:
        raise e
