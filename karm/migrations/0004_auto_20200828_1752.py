# Generated by Django 3.0.3 on 2020-08-28 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('karm', '0003_auto_20200828_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='username',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
