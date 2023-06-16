from rest_framework import serializers

from kyiv_weather.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ("id", "date", "temperature", "description")


class TaskSerializer(serializers.Serializer):
    minute = serializers.CharField(max_length=60, required=False, default="0")
    hour = serializers.CharField(max_length=24, required=False, default="9")
    day_of_week = serializers.CharField(max_length=7, required=False, default="*")
    day_of_month = serializers.CharField(max_length=31, required=False, default="*")
    month_of_year = serializers.CharField(max_length=12, required=False, default="*")
