# Generated by Django 4.0.2 on 2022-06-18 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0025_subject_dept_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackstaff',
            name='dept_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Student.department'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedbackstudent',
            name='dept_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Student.department'),
            preserve_default=False,
        ),
    ]
