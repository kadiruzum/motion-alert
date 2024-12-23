# Generated by Django 5.1.4 on 2024-12-21 21:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("detection", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MotionEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("motion_start_time", models.DateTimeField()),
                ("motion_end_time", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name="MotionDetection",
        ),
    ]
