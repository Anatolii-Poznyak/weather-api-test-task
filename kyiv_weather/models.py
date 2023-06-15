from django.db import models


class Weather(models.Model):
    date = models.DateField()
    temperature = models.IntegerField()
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "weather"

    def __str__(self):
        return f"{self.date}: {self.temperature}. {self.description}"
