# Generated by Django 5.0 on 2024-04-07 17:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_class_class_teacher_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='class_teacher_id',
        ),
        migrations.AddField(
            model_name='class',
            name='class_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
