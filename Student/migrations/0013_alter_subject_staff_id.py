# Generated by Django 4.0.2 on 2022-06-12 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0012_alter_subject_staff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='staff_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
