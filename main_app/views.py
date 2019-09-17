from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import View

from data_app.calculator.all_games import get_rank_result
from data_app.models import Champion, Summoner, RankGameResult, Score

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
            context['summoner'] = summoner
            context['rank_result'] = RankGameResult.objects.filter(summoner=summoner)

        else:
            print('exist')
            # RankGameResult.objects.filter(summoner=summoner).delete()
            # self.create_rank_result(result, summoner)
            summoner.refreshed_date = timezone.now()
            summoner.save()
            context['summoner'] = summoner
            context['rank_result'] = RankGameResult.objects.filter(summoner=summoner)

        score_dict = {}
        score_object = Score.objects.filter(target=summoner)
        score_count = score_object.count()
        score_sum = score_object.aggregate(Sum('score'))
        print(score_sum)
        print(score_count)
        if score_count > 0:
            score_dict['average'] = round(score_sum['score__sum'] / score_count, 2)
            score_dict['count'] = score_count
        else:
            score_dict['average'] = None
            score_dict['count'] = None
        context['score'] = score_dict

        if self.request.user.is_authenticated:
            exist = Score.objects.filter(valuer=self.request.user).exists()
        else:
            exist = Score.objects.filter(ip_addr=self.request.session._session['ip']).exists()

        if exist:
            score_dict['already'] = True
        else:
            score_dict['already'] = False

        return render(request=self.request, context=context, template_name='search/summoner.html')
