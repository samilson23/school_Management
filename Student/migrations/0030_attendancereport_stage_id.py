# Generated by Django 4.0.2 on 2022-06-22 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0029_students_stage_id_students_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancereport',
            name='stage_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Student.semester'),
        ),
    ]
