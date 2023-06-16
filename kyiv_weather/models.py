from django.db import models


class Weather(models.Model):
    date = models.DateField()
    temperature = models.IntegerField()
    description = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        existing_weather = Weather.objects.filter(date=self.date).first()
        if existing_weather:
            self.pk = existing_weather.pk
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date}: {self.temperature}. {self.description}"

    class Meta:
        verbose_name_plural = "weather"
