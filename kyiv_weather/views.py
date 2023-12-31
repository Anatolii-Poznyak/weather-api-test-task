from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter

from kyiv_weather.models import Weather
from kyiv_weather.serializers import WeatherSerializer, TaskSerializer
from kyiv_weather.tasks import main_task, update_weather


class WeatherPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 25


class WeatherListView(ListAPIView):
    queryset = Weather.objects.order_by("date")
    serializer_class = WeatherSerializer
    pagination_class = WeatherPagination


@extend_schema(
    methods=["POST"],
    request=TaskSerializer,
    responses={200: {"message": "string"}},
)
@api_view(["POST"])
def schedule_task(request: Request) -> Response:
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


@extend_schema(
    methods=["POST"],
    responses={
        200: {
            "task_id": "string",
            "task_status_url": "string",
            "message": "string"
        }
    }
)
@api_view(["POST"])
def weather_update(request: Request) -> Response:
    task = update_weather.delay()
    task_status_url = request.build_absolute_uri(
        f"/kyiv_weather/get_task_status/{task.id}/"
    )
    return Response(
        {
            "task_id": task.id,
            "task_status_url": task_status_url,
            "message": "Weather update has been started !",
        }
    )


@extend_schema(
    methods=["GET"],
    parameters=[
        OpenApiParameter(
            name="task_id",
            description="Task ID for which to get the status",
            required=True,
            type=str
        )
    ],
    responses={200: {"task_id": "string", "status": "string"}},
)
@api_view(["GET"])
def get_task_status(request: Request, task_id: str) -> Response:
    task = AsyncResult(task_id)
    return Response({"task_id": task_id, "status": task.status})
