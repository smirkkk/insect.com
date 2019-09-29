# Generated by Django 2.2.4 on 2019-09-29 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0018_auto_20190929_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='badge1',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='badge1', to='data_app.Badge'),
        ),
        migrations.AddField(
            model_name='summoner',
            name='badge2',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='badge2', to='data_app.Badge'),
        ),
        migrations.AddField(
            model_name='summoner',
            name='badge3',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='badge3', to='data_app.Badge'),
        ),
    ]
