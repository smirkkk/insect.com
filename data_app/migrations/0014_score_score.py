# Generated by Django 2.2.4 on 2019-09-17 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0013_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
