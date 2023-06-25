from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from django_celery_beat.models import PeriodicTask

from kyiv_weather.tasks import main_task


class TaskCommandTest(TestCase):
    @mock.patch("kyiv_weather.tasks.main_task")
    def test_handle_executes_main_task(self, mock_main_task):
        test_hour = "12"
        call_command("task_command", hour=test_hour)
        mock_main_task.assert_called_once_with(hour=test_hour)

    def test_main_task_creates_periodic_task(self):
        test_hour = "13"
        main_task(hour=test_hour)

        periodic_task = PeriodicTask.objects.last()
        self.assertIsNotNone(periodic_task)
        self.assertEqual(periodic_task.crontab.hour, test_hour)

    def test_main_task_default_hour(self):
        main_task()

        periodic_task = PeriodicTask.objects.last()
        self.assertIsNotNone(periodic_task)
        self.assertEqual(periodic_task.crontab.hour, "9")
