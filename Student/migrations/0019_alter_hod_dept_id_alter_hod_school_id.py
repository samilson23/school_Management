# Generated by Django 4.0.2 on 2022-06-18 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0018_department_school_hod_dept_id_hod_school_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hod',
            name='dept_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Student.department'),
        ),
        migrations.AlterField(
            model_name='hod',
            name='school_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Student.school'),
        ),
    ]
