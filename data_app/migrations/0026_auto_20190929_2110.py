# Generated by Django 2.2.4 on 2019-09-29 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0025_summoner_badge1'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='badge4',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='badge4', to='data_app.Badge'),
        ),
        migrations.AddField(
            model_name='summoner',
            name='badge5',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='badge5', to='data_app.Badge'),
        ),
    ]
