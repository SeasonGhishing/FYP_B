# Generated by Django 5.0 on 2024-04-20 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0009_alter_announcement_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 21, 0, 7, 9, 61639)),
        ),
    ]
