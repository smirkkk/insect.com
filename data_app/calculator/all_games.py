import datetime
import time

import pymysql
import requests

from data_app.models import Summoner




# 소환사 정보
def get_summoner_info(summoner_name):
    # 입력받은 소환사 이름
    summoner_name = summoner_name.replace(' ', '')

    # api로부터 소환사 정보 parse
    summoner_object = requests.get(
        'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(summoner_name, api_key))
    summoner_object = summoner_object.json()

    print(summoner_object)

    # accountId로 존재하는 소환사인지 아닌지 판단
    summoner, created = Summoner.objects.get_or_create(account_id=summoner_object['accountId'])

    # 소환사 이름 등 갱신
    summoner.summoner_name = summoner_object['name']
    summoner.summoner_id = summoner_object['id']
    summoner.icon = summoner_object['profileIconId']
    summoner.level = summoner_object['summonerLevel']

    # summonerId로 소환사 랭크 게임 정보 parse
    rank_tier_object = requests.get(
        'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}'.format(summoner_object['id'],
                                                                                              api_key))
    rank_tier_object = rank_tier_object.json()

    for x in rank_tier_object:
        # 솔랭 5대5만 기록
        if x['queueType'] == 'RANKED_SOLO_5x5':
            summoner.rank = x['rank']
            summoner.tier = x['tier']

    summoner.save()

    return summoner, summoner_object


# 소환사 훈장
# 1 : 평점 높으면 2: 평점 낮으면 3: 게임 수 많으면 4: 승률 높으면 5: 승률 낮으면 6-15: 챌-아,언랭
def set_summoner_badge(summoner):

    rank_result_sum = RankGameResult.objects.filter(summoner=summoner).aggregate(Sum('games'), Sum('kills'),
                                                                                 Sum('deaths'), Sum('assists'),
                                                                                 Sum('winning_rate'))
    champions = RankGameResult.objects.filter(summoner=summoner).count()

    games = rank_result_sum['games__sum']
    average = (rank_result_sum['kills__sum'] + rank_result_sum['assists__sum']) / rank_result_sum['deaths__sum']
    winning_rate = rank_result_sum['winning_rate__sum'] / champions

    print(games, average, winning_rate)

    if average >= 3:
        summoner.badge1 = Badge.objects.get(id=1)
    elif average <= 2:
        summoner.badge1 = Badge.objects.get(id=2)

    if games >= 350:
        summoner.badge2 = Badge.objects.get(id=3)

    if winning_rate >= 60:
        summoner.badge3 = Badge.objects.get(id=4)
    elif winning_rate <= 45:
        summoner.badge3 = Badge.objects.get(id=5)

    if summoner.tier == 'CHALLENGER':
        summoner.badge4 = Badge.objects.get(id=6)
    elif summoner.tier == 'GRANDMASTER':
        summoner.badge4 = Badge.objects.get(id=7)
    elif summoner.tier == 'MASTER':
        summoner.badge4 = Badge.objects.get(id=8)
    elif summoner.tier == 'DIAMOND':
        summoner.badge4 = Badge.objects.get(id=9)
    elif summoner.tier == 'PLATINUM':
        summoner.badge4 = Badge.objects.get(id=10)
    elif summoner.tier == 'GOLD':
        summoner.badge4 = Badge.objects.get(id=11)
    elif summoner.tier == 'SILVER':
        summoner.badge4 = Badge.objects.get(id=12)
    elif summoner.tier == 'BRONZE':
        summoner.badge4 = Badge.objects.get(id=13)
    elif summoner.tier == 'IRON':
        summoner.badge4 = Badge.objects.get(id=14)
    else:
        print('언랭련')
        summoner.badge4 = Badge.objects.get(id=15)

    summoner.save()
    return summoner


# 랭크 게임 match list
def get_match_list(summoner_object, season, queue, total_games):
    result = []
    li = 0
    while True:
        time.sleep(1)
        match_list = requests.get(
            'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?season={}&queue={}&beginIndex={}&api_key={}'.format(
                summoner_object['accountId'], season, queue, str(li * 100), api_key)).json()
        if match_list['matches']:
            for y in match_list['matches']:
                result.append(y['gameId'])
        else:
            print(queue, ' end')
            break
        li += 1

    return result


# 랭크 게임
def get_rank_result(summoner_name):
    # 입력받은 소환사 이름
    summoner_name = summoner_name.replace(' ', '')
    summoner, summoner_object = get_summoner_info(summoner_name)

    # 전체 랭크 게임 parse
    # 2019년 season 13
    # queue 420, 440
    total_games = requests.get('https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?season=13&queue=420&endIndex=100&api_key={}'.format(summoner_object['accountId'], api_key))
    total_games_duo = requests.get('https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?season=13&queue=440&endIndex=100&api_key={}'.format(summoner_object['accountId'], api_key))
    try:
        total_games = int(total_games.json()['totalGames'])
        total_games_duo = int(total_games_duo.json()['totalGames'])
    except KeyError as e:
        print('No Rank Game')

    match_id_list = []

    solo_result = get_match_list(summoner_object, 13, 420, total_games)
    match_id_list += solo_result
    duo_result = get_match_list(summoner_object, 13, 440, total_games_duo)
    match_id_list += duo_result

    champion_dict = {}

    print('총 게임 수 : ', len(match_id_list))

    start = datetime.datetime.now()
    print(start)
    for index, match_id in enumerate(match_id_list):
        print(str(index), 'of', str(len(match_id_list)))
        time.sleep(1)
        game_result = requests.get(
            'https://kr.api.riotgames.com/lol/match/v4/matches/{}?api_key={}'.format(
                str(match_id), api_key)).json()

        for participantIdentities in game_result['participantIdentities']:
            if participantIdentities['player']['accountId'] == summoner_object['accountId']:
                participantId = participantIdentities['participantId']
                break

        for participant in game_result['participants']:
            if participant['participantId'] == participantId:
                # 이미 해당 챔피언에 대해 집계를 했을 경우
                if participant['championId'] in champion_dict.keys():
                    champion_dict[participant['championId']]['kills'] += participant['stats']['kills']
                    champion_dict[participant['championId']]['deaths'] += participant['stats']['deaths']
                    champion_dict[participant['championId']]['assists'] += participant['stats']['assists']
                    champion_dict[participant['championId']]['games'] += 1

                    if participant['stats']['win']:
                        champion_dict[participant['championId']]['win'] += 1
                    else:
                        champion_dict[participant['championId']]['lose'] += 1

                # 새로운 챔피언에 대해 집계할 경우
                else:
                    tmp_dict = {
                                'kills': participant['stats']['kills'],
                                'deaths': participant['stats']['deaths'],
                                'assists': participant['stats']['assists'],
                                'games': 1
                                }
                    if participant['stats']['win']:
                        tmp_dict['win'] = 1
                        tmp_dict['lose'] = 0
                    else:
                        tmp_dict['lose'] = 1
                        tmp_dict['win'] = 0
                    champion_dict[participant['championId']] = tmp_dict

    print(str(datetime.datetime.now() - start))
    set_summoner_badge(summoner)

    result_dict = {'summoner': summoner_object, 'rank_result': champion_dict}
    summoner.refreshed_date = timezone.now()
    summoner.save()

    return result_dict
