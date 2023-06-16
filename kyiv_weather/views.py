from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from kyiv_weather.models import Weather
from kyiv_weather.serializers import WeatherSerializer, TaskSerializer
from kyiv_weather.tasks import main_task, update_weather


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
    update_weather()
    return Response({"message": "Weather updated !"})
