# Generated by Django 5.1.4 on 2024-12-21 21:14

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MotionDetection",
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
                ("video_name", models.CharField(max_length=255)),
                ("motion_start_time", models.DateTimeField()),
                ("motion_end_time", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
