# Generated by Django 5.0 on 2024-04-07 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='class_teacher_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
