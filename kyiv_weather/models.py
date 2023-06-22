from django.db import models


class Weather(models.Model):
    date = models.DateField()
    temperature = models.IntegerField()
    description = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        Weather.objects.update_or_create(
            date=self.date,
            defaults={
                "temperature": self.temperature,
                'description': self.description
            }
        )

    def __str__(self):
        return f"{self.date}: {self.temperature}. {self.description}"

    class Meta:
        verbose_name_plural = "weather"
