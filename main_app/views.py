from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import View

from data_app.calculator.all_games import get_rank_result
from data_app.models import Champion, Summoner, RankGameResult

# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'


class SearchView(View):
    def create_rank_result(self, result, summoner):
        for rank_result_champion in result['rank_result'].keys():
            champion = get_object_or_404(Champion, champion_key=rank_result_champion)

            win = result['rank_result'][rank_result_champion]['win']
            lose = result['rank_result'][rank_result_champion]['lose']
            games = result['rank_result'][rank_result_champion]['games']
            kills = result['rank_result'][rank_result_champion]['kills']
            deaths = result['rank_result'][rank_result_champion]['deaths']
            assists = result['rank_result'][rank_result_champion]['assists']

            try:
                average = round((result['rank_result'][rank_result_champion]['kills'] +
                                 result['rank_result'][rank_result_champion]['assists']) /
                                result['rank_result'][rank_result_champion]['deaths'], 2)
            except ZeroDivisionError:
                average = None

            winning_rate = round(
                result['rank_result'][rank_result_champion]['win'] / result['rank_result'][rank_result_champion][
                    'games'] * 100)

            RankGameResult.objects.create(champion=champion, summoner=summoner,
                                          win=win,
                                          lose=lose,
                                          games=games,
                                          kills=kills,
                                          deaths=deaths,
                                          assists=assists,
                                          average=average,
                                          winning_rate=winning_rate
                                          )

    def get(self, request, *args, **kwargs):
        context = {}
        summoner_name = self.request.GET.get('summoner_name')
        print(summoner_name)
        # result = get_rank_result(summoner_name)

        summoner, created = Summoner.objects.get_or_create(summoner_name=summoner_name)
        # summoner, created = Summoner.objects.get_or_create(summoner_name=result['summoner']['name'],
                                       # account_id=result['summoner']['accountId'])

        if created:
            print('created')
            # for rank_result_champion in result['rank_result'].keys():
            #    self.create_rank_result(result, created)
            #    champion = get_object_or_404(Champion, champion_key=rank_result_champion)
            context['summoner'] = created
            context['rank_result'] = RankGameResult.objects.filter(summoner=created)

        else:
            print('exist')
            # RankGameResult.objects.filter(summoner=summoner).delete()
            # self.create_rank_result(result, summoner)
            summoner.refreshed_date = timezone.now()
            summoner.save()
            context['summoner'] = summoner
            context['rank_result'] = RankGameResult.objects.filter(summoner=summoner)

        return render(request=self.request, context=context, template_name='search/result.html')
