# Generated by Django 5.0 on 2024-04-10 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave_requests', '0002_leaverequest_assigned_class_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaverequest',
            name='assigned_class_name',
        ),
    ]
