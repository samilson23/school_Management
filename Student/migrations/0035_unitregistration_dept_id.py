# Generated by Django 4.0.2 on 2022-06-26 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0034_alter_attendancereport_stage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitregistration',
            name='dept_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Student.department'),
        ),
    ]
