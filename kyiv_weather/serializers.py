from rest_framework import serializers

from kyiv_weather.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ("id", "date", "temperature", "description")
