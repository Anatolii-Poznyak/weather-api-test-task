from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from kyiv_weather.models import Weather
from kyiv_weather.serializers import WeatherSerializer
from scraper import sync_weather

class WeatherListView(ListAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
