from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Champion(models.Model):
    champion_key = models.IntegerField(default=None, null=True, blank=True)
    champion_name = models.CharField(default=None, null=True, blank=True, max_length=20)
    champion_english_name = models.CharField(default=None, null=True, blank=True, max_length=20)
    champion_brood = models.CharField(default=None, null=True, blank=True, max_length=50)
    champion_title = models.CharField(default=None, null=True, blank=True, max_length=50)
    champion_short = models.CharField(default=None, null=True, blank=True, max_length=10)

    # 승률 60% 이상
    grade1 = models.CharField(default=None, null=True, blank=True, max_length=200)  # 평점 4점 이상
    grade2 = models.CharField(default=None, null=True, blank=True, max_length=200)  # 평점 3점대
    grade3 = models.CharField(default=None, null=True, blank=True, max_length=200)  # 평점 2점대
    grade4 = models.CharField(default=None, null=True, blank=True, max_length=200)  # 평점 1점대
    grade5 = models.CharField(default=None, null=True, blank=True, max_length=200)  # 평점 1점 미만

    # 승률 50% 대
    grade6 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade7 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade8 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade9 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade10 = models.CharField(default=None, null=True, blank=True, max_length=200)

    # 승률 40% 대
    grade11 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade12 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade13 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade14 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade15 = models.CharField(default=None, null=True, blank=True, max_length=200)

    # 승률 40% 미만
    grade16 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade17 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade18 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade19 = models.CharField(default=None, null=True, blank=True, max_length=200)
    grade20 = models.CharField(default=None, null=True, blank=True, max_length=200)

    def __str__(self):
        return self.champion_name
    
    class Meta:
        db_table = 'data_champion'


class Summoner(models.Model):
    account_id = models.CharField(default=None, null=True, blank=True, max_length=200)
    summoner_name = models.CharField(default=None, null=True, blank=True, max_length=50)
    tier = models.CharField(default=None, null=True, blank=True, max_length=20)
    refreshed_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'data_summoner'


class RankGameResult(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    win = models.IntegerField(default=None, null=True, blank=True)
    lose = models.IntegerField(default=None, null=True, blank=True)
    kills = models.IntegerField(default=None, null=True, blank=True)
    deaths = models.IntegerField(default=None, null=True, blank=True)
    assists = models.IntegerField(default=None, null=True, blank=True)
    games = models.IntegerField(default=None, null=True, blank=True)
    winning_rate = models.IntegerField(default=None, null=True, blank=True)
    average = models.FloatField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'data_rank_result'


class Comment(models.Model):
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300, default=None, null=True, blank=True)
    password = models.TextField(max_length=30, default=None, null=True, blank=True)
    writer = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)  # 로그인 한 경우
    ip_addr = models.TextField(max_length=16, null=True, blank=True, default=None)  # 로그인 안 한 경우
    nickname = models.TextField(max_length=50, null=True, blank=True, default=None)  # 로그인 안 한 경우
    written_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    like = models.IntegerField(default=0, null=True, blank=True)
    dislike = models.IntegerField(default=0, null=True, blank=True)
    total = models.IntegerField(default=0, null=True, blank=True)
    blind_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'data_comment'


class CommentReport(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reported_comment')
    reporter = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)  # 로그인 한 경우
    ip_addr = models.TextField(max_length=16, null=True, blank=True, default=None)  # 로그인 안 한 경우
    report_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    reason = models.TextField(max_length=200, default=None, null=True, blank=True)

    class Meta:
        db_table = 'data_comment_report'


class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='target_comment')
    liker = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)  # 로그인 한 경우
    ip_addr = models.TextField(max_length=16, null=True, blank=True, default=None)  # 로그인 안 한 경우
    liked_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    like = models.BooleanField(default=False, null=True, blank=True)
    dislike = models.IntegerField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'data_like'

    def __str__(self):
        return self.comment


class Score(models.Model):
    target = models.ForeignKey(Summoner, on_delete=models.CASCADE, related_name='score_target')
    score = models.IntegerField(default=0, null=True, blank=True)
    valuer = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)  # 로그인 한 경우
    ip_addr = models.TextField(max_length=16, null=True, blank=True, default=None)  # 로그인 안 한 경우
    score_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = 'data_summoner_score'
