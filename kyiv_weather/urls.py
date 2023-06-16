from django.urls import path

from kyiv_weather.views import WeatherListView, schedule_task, weather_update

urlpatterns = [
    path("", WeatherListView.as_view(), name="weather-list"),
    path("schedule_task/", schedule_task, name="schedule-task"),
    path("weather_update/", weather_update, name="weather-update"),
]

app_name = "kyiv_weather"
