# Generated by Django 4.0.2 on 2022-06-18 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0019_alter_hod_dept_id_alter_hod_school_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='school_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Student.school'),
        ),
        migrations.AlterField(
            model_name='hod',
            name='dept_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Student.department'),
        ),
        migrations.AlterField(
            model_name='hod',
            name='school_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Student.school'),
        ),
    ]
