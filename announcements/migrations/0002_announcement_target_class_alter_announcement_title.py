# Generated by Django 5.0 on 2024-02-13 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='target_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.class'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
