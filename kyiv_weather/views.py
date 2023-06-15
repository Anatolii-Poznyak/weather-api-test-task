from rest_framework.generics import ListAPIView
from django.shortcuts import render

from kyiv_weather.models import Weather
from kyiv_weather.serializers import WeatherSerializer


class WeatherListView(ListAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
