import random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from data_app.models import Champion


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'account_profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            while True:
                emotion = random.choice(list(NicknameEmotion.objects.values('emotion')))
                champ = random.choice(list(Champion.objects.values('champion_short')))
                nickname = emotion['emotion'] + ' ' + champ['champion_short']
                if Profile.objects.filter(nickname=nickname).exists() or NonMemberSession.objects.filter(nickname=nickname).exists():
                    pass
                else:
                    Profile.objects.create(user=instance, nickname=nickname)
                    break

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class NicknameEmotion(models.Model):
    emotion = models.CharField(max_length=10, default=None, null=True, blank=True, unique=True)

    def __str__(self):
        return self.emotion

    class Meta:
        db_table = 'account_nick_emotion'


class NonMemberSession(models.Model):
    ip = models.CharField(max_length=16, default=None, null=True, blank=True, unique=True)
    nickname = models.CharField(max_length=50, null=True, blank=True, default=None)
    last_use = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'account_non_member_session'
