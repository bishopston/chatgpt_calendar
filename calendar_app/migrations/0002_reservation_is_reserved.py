# Generated by Django 4.2.6 on 2023-11-06 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
    ]
