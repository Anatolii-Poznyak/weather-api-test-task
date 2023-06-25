from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import APIClient

from kyiv_weather.models import Weather
from kyiv_weather.views import (
    WeatherListView,
)


class WeatherListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = WeatherListView.as_view()
        self.uri = reverse("kyiv_weather:weather-list")

        # Create some test data
        Weather.objects.create(date="2023-06-01", temperature=20, description="sunny")
        Weather.objects.create(date="2023-06-02", temperature=25, description="cloudy")

    def test_retrieve_weather_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_weather_list_sorted_by_date(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.data["results"]),
            sorted(response.data["results"], key=lambda weather: weather["date"]),
        )

    def test_retrieve_empty_weather_list(self):
        Weather.objects.all().delete()
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)


class ScheduleTaskTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = reverse("kyiv_weather:schedule-task")

    def test_schedule_task_success(self):
        data = {
            "minute": "0",
            "hour": "9",
            "day_of_week": "*",
            "day_of_month": "*",
            "month_of_year": "*",
        }
        response = self.client.post(self.uri, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Task was scheduled !"})

    def test_schedule_task_invalid_input(self):
        data = {
            "minute": "0",
            "hour": "invalid",
            "day_of_week": "*",
            "day_of_month": "*",
            "month_of_year": "*",
        }
        response = self.client.post(self.uri, data, format="json")
        self.assertEqual(response.status_code, 400)


class WeatherUpdateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = reverse("kyiv_weather:weather-update")

    def test_weather_update_success(self):
        response = self.client.post(self.uri)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("task_id" in response.data)
        self.assertTrue("task_status_url" in response.data)
        self.assertEqual(response.data["message"], "Weather update has been started !")


class GetTaskStatusTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = reverse(
            "kyiv_weather:get-task-status", kwargs={"task_id": "test_id"}
        )

    def test_get_task_status(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["task_id"], "test_id")
        self.assertTrue("status" in response.data)
