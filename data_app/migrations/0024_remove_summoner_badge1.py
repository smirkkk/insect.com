# Generated by Django 2.2.4 on 2019-09-29 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0023_auto_20190929_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summoner',
            name='badge1',
        ),
    ]
