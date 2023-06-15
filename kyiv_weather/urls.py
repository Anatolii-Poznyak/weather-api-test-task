from django.urls import path

from kyiv_weather.views import WeatherListView

urlpatterns = [
    path("", WeatherListView.as_view(), name="weather-list")
]

app_name = "kyiv_weather"
