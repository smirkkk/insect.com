# Generated by Django 2.2.4 on 2019-09-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member_app', '0002_nicknameemotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nicknameemotion',
            name='emotion',
            field=models.CharField(blank=True, default=None, max_length=10, null=True, unique=True),
        ),
    ]