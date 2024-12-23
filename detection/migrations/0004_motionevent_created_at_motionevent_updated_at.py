# Generated by Django 5.1.4 on 2024-12-23 08:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("detection", "0003_alter_motionevent_motion_end_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="motionevent",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="motionevent",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
