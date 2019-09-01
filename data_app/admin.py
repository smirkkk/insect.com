from django.contrib import admin
from .models import Champion
from .forms import ChampionForm

# Register your models here.


class ChampionAdmin(admin.ModelAdmin):
    form = ChampionForm

    fieldsets = [
        (None,               {'fields': ['champion_key', 'champion_name', 'champion_brood', 'champion_title']}),
        ('승률 60% 이상', {'fields': ['grade1', 'grade2', 'grade3', 'grade4', 'grade5']}),
        ('승률 50%대', {'fields': ['grade6', 'grade7', 'grade8', 'grade9', 'grade10']}),
        ('승률 40%대', {'fields': ['grade11', 'grade12', 'grade13', 'grade14', 'grade15']}),
        ('승률 40%미만', {'fields': ['grade16', 'grade17', 'grade18', 'grade19', 'grade20']}),
    ]


admin.site.register(Champion, ChampionAdmin)
