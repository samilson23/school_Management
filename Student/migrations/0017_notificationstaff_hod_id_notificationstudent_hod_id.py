# Generated by Django 4.0.2 on 2022-06-17 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0016_notificationstudent_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationstaff',
            name='Hod_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notificationstudent',
            name='Hod_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
