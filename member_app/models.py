from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'account_profile'


class NicknameEmotion(models.Model):
    emotion = models.CharField(max_length=10, default=None, null=True, blank=True)

    class Meta:
        db_table = 'account_nick_emotion'
