# Generated by Django 5.0 on 2024-04-08 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_remove_class_class_teacher_id_class_class_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='class_teacher',
        ),
        migrations.AddField(
            model_name='class',
            name='teacher_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
