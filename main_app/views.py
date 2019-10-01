import json

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import View

from data_app.calculator.all_games import get_rank_result, get_summoner_info
from data_app.models import Champion, Summoner, RankGameResult, Score

# Create your views here.
from django.views.generic import TemplateView


def create_rank_result(result, summoner):
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


class IndexView(TemplateView):
    template_name = 'main/index.html'


class SearchView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        summoner_name = self.request.GET.get('summoner_name')
        print(summoner_name)

        summoner, trash = get_summoner_info(summoner_name)
        last_refresh = timezone.now() - summoner.refreshed_date
        print(summoner.refreshed_date)
        print(timezone.now())
        print(last_refresh.days)

        if last_refresh.days >= 7:
            # 갱신 시간별로 삭제하고 새로 조회할지 냅둘지 만들어야함
            result = get_rank_result(summoner_name)
            RankGameResult.objects.filter(summoner=summoner).delete()
            create_rank_result(result, summoner)
            summoner.refreshed_date = timezone.now()
            summoner.save()
        else:
            pass
        context['summoner'] = summoner
        context['rank_result'] = RankGameResult.objects.filter(summoner=summoner).order_by('-games')

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
            exist = Score.objects.filter(valuer=self.request.user, target=summoner).exists()
        else:
            exist = Score.objects.filter(ip_addr=self.request.session._session['ip'], target=summoner).exists()

        if exist:
            score_dict['already'] = True
        else:
            score_dict['already'] = False

        return render(request=self.request, context=context, template_name='search/summoner.html')


class RefreshView(View):
    def post(self, request):
        context = {}
        summoner_name = self.request.POST.get('summoner_name')
        summoner, trash = get_summoner_info(summoner_name)

        result = get_rank_result(summoner_name)
        RankGameResult.objects.filter(summoner=summoner).delete()
        create_rank_result(result, summoner)
        summoner.refreshed_date = timezone.now()
        summoner.save()

        return HttpResponse(json.dumps(context), content_type="application/json")
