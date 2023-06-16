from django.urls import path

from kyiv_weather.views import WeatherListView, schedule_task, weather_update, get_task_status

urlpatterns = [
    path("", WeatherListView.as_view(), name="weather-list"),
    path("schedule_task/", schedule_task, name="schedule-task"),
    path("weather_update/", weather_update, name="weather-update"),
    path("get_task_status/<str:task_id>/", get_task_status, name="get-task-status"),
]

app_name = "kyiv_weather"
