# Generated by Django 4.0.2 on 2022-06-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0023_students_dept_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='dept_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Student.department'),
        ),
    ]