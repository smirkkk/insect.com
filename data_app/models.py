from django.db import models

# Create your models here.


class Champion(models.Model):
    champion_key = models.IntegerField(default=None, null=True, blank=True)
    champion_name = models.CharField(default=None, null=True, blank=True, max_length=20)
    champion_brood = models.CharField(default=None, null=True, blank=True, max_length=50)
    champion_title = models.CharField(default=None, null=True, blank=True, max_length=50)

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
