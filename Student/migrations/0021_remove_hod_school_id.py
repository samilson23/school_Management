# Generated by Django 4.0.2 on 2022-06-18 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0020_department_school_id_alter_hod_dept_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hod',
            name='school_id',
        ),
    ]
