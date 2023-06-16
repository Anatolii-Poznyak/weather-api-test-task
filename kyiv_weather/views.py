

from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from kyiv_weather.models import Weather
from kyiv_weather.serializers import WeatherSerializer, TaskSerializer
from kyiv_weather.tasks import main_task, update_weather
from celery.result import AsyncResult


class WeatherListView(ListAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer


@api_view(["POST"])
def schedule_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        minute = serializer.validated_data.get("minute", "0")
        hour = serializer.validated_data.get("hour", "9")
        day_of_week = serializer.validated_data.get("day_of_week", "*")
        day_of_month = serializer.validated_data.get("day_of_month", "*")
        month_of_year = serializer.validated_data.get("month_of_year", "*")
        main_task(minute, hour, day_of_week, day_of_month, month_of_year)
        return Response({"message": "Task was scheduled !"})
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def weather_update(request):
    task = update_weather.apply_async(countdown=15) # FIXME FOR TESTING
    # task = update_weather.delay()
    task_status_url = request.build_absolute_uri(f"/kyiv_weather/get_task_status/{task.id}/")
    return Response(
        {"task_id": task.id, "task_status_url": task_status_url, "message": "Weather update has been started !"}
    )


@api_view(["GET"])
def get_task_status(request, task_id):
    task = AsyncResult(task_id)
    return Response({
        "task_id": task_id,
        "status": task.status
    })
