# Generated by Django 5.0 on 2024-04-20 18:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0008_alter_announcement_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 21, 0, 2, 15, 442750)),
        ),
    ]
