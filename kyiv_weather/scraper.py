from datetime import date, timedelta

import cloudscraper
from bs4 import BeautifulSoup

from config.settings import KYIV_WEATHER_API_URL
from kyiv_weather.models import Weather


def parse_weather() -> list[Weather]:
    scraper = cloudscraper.create_scraper()
    page = scraper.get(KYIV_WEATHER_API_URL).content

    soup = BeautifulSoup(page, "html.parser")

    five_days = soup.select(".five-days__day.fl-col")
    start_date = date.today()

    return [
        Weather(
            date=start_date + timedelta(days=index),
            temperature=int(day.select_one(".high").text.replace("°", "")),
            description=day.select_one(".five-days__icon")["data-tippy-content"],
        )
        for index, day in enumerate(five_days)
    ]


def save_weather(five_days_weather: list[Weather]) -> None:
    for one_day_weather in five_days_weather:
        one_day_weather.save()


def sync_weather() -> None:
    weather = parse_weather()
    save_weather(weather)

