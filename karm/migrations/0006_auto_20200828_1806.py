# Generated by Django 3.0.3 on 2020-08-28 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karm', '0005_auto_20200828_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='authority',
            field=models.CharField(default='no auth', max_length=20),
        ),
        migrations.AddField(
            model_name='doctor',
            name='specialization',
            field=models.CharField(default='heart', max_length=50),
        ),
    ]
