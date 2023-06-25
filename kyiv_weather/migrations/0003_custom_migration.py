from django.core.management import call_command
from django.db import migrations


def create_superuser(apps, schema_editor):
    call_command("create_superuser")


class Migration(migrations.Migration):

    dependencies = [
        ("kyiv_weather", "0002_alter_weather_options"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
