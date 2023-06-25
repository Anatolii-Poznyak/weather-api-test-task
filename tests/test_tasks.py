from unittest.mock import patch, Mock

from django.test import TestCase
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from kyiv_weather.exceptions import NetworkError
from kyiv_weather.tasks import update_weather, main_task


class TasksTest(TestCase):
    @patch("kyiv_weather.tasks.sync_weather")
    def test_update_weather_calls_sync_weather(self, mock_sync_weather):
        update_weather()
        mock_sync_weather.assert_called_once()

    def test_main_task_creates_new_periodic_task(self):
        main_task("1", "2", "3", "4", "5")
        schedule = CrontabSchedule.objects.get(
            minute="1", hour="2", day_of_week="3", day_of_month="4", month_of_year="5"
        )
        task = PeriodicTask.objects.get(
            crontab=schedule, task="kyiv_weather.tasks.my_task_weather"
        )
        self.assertEqual(task.name, "Weather daily update")

    def test_main_task_updates_existing_task(self):
        schedule_1, _ = CrontabSchedule.objects.get_or_create(
            minute="1", hour="2", day_of_week="3", day_of_month="4", month_of_year="5"
        )
        schedule_2, _ = CrontabSchedule.objects.get_or_create(
            minute="1", hour="2", day_of_week="3", day_of_month="4", month_of_year="6"
        )
        PeriodicTask.objects.create(
            crontab=schedule_1,
            name="Weather daily update",
            task="kyiv_weather.tasks.my_task_weather",
            args="[]",
        )

        main_task("1", "2", "3", "4", "6")

        task = PeriodicTask.objects.get(name="Weather daily update")
        self.assertEqual(task.crontab, schedule_2)

    @patch("django_celery_beat.models.CrontabSchedule.objects.get_or_create")
    @patch("django_celery_beat.models.PeriodicTask.objects.get_or_create")
    def test_main_task_creates_periodic_task_with_crontab_schedule(
        self, mock_periodic_get_or_create, mock_crontab_get_or_create
    ):
        mock_crontab_schedule = Mock()
        mock_crontab_get_or_create.return_value = mock_crontab_schedule, False
        mock_periodic_task = Mock()
        mock_periodic_get_or_create.return_value = mock_periodic_task, False
        main_task("0", "9", "*", "*", "*")
        mock_crontab_get_or_create.assert_called_once()
        mock_periodic_get_or_create.assert_called_once_with(
            name="Weather daily update",
            defaults={
                "crontab": mock_crontab_schedule,
                "task": "kyiv_weather.tasks.my_task_weather",
                "args": "[]",
            },
        )
        self.assertEqual(mock_periodic_task.crontab, mock_crontab_schedule)
        mock_periodic_task.save.assert_called_once()

    @patch("kyiv_weather.tasks.PeriodicTask")
    @patch("kyiv_weather.tasks.CrontabSchedule")
    def test_main_task_does_not_save_existing_task(
        self, mock_crontab_schedule, mock_periodic_task
    ):
        mock_schedule = Mock()
        mock_crontab_schedule.objects.get_or_create.return_value = (mock_schedule, True)
        mock_task = Mock()
        mock_periodic_task.objects.get_or_create.return_value = (mock_task, True)

        main_task(
            minute="0", hour="10", day_of_week="*", day_of_month="*", month_of_year="*"
        )

        mock_crontab_schedule.objects.get_or_create.assert_called_once_with(
            minute="0", hour="10", day_of_week="*", day_of_month="*", month_of_year="*"
        )
        mock_periodic_task.objects.get_or_create.assert_called_once_with(
            name="Weather daily update",
            defaults={
                "crontab": mock_schedule,
                "task": "kyiv_weather.tasks.my_task_weather",
                "args": "[]",
            },
        )
        assert not mock_task.save.called

    @patch("kyiv_weather.tasks.sync_weather")
    def test_update_weather_handles_network_error(self, mock_sync_weather):
        mock_sync_weather.side_effect = NetworkError("Network error")
        with self.assertRaises(NetworkError):
            update_weather()
