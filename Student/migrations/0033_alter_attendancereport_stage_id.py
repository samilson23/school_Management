# Generated by Django 4.0.2 on 2022-06-22 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0032_alter_attendancereport_stage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancereport',
            name='stage_id',
            field=models.CharField(max_length=10),
        ),
    ]
