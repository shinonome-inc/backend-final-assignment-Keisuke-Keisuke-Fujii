# Generated by Django 4.1.4 on 2023-06-18 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_friendship_friendship_unique_friendship"),
    ]

    operations = [
        migrations.AlterField(
            model_name="friendship",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="following", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="friendship",
            name="following",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="follower", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]