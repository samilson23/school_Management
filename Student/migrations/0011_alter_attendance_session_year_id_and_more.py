# Generated by Django 4.0.2 on 2022-06-12 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0010_alter_studentresult_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='session_year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Student.sessionmodel'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.subject'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='course_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Student.courses'),
        ),
    ]