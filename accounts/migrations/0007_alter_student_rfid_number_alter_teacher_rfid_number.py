# Generated by Django 5.0 on 2024-03-14 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_apikey_device_name_alter_apikey_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='rfid_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='rfid_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
