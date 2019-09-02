import time

import pymysql
import requests



def get_rank_result(summoner_name):
    summoner_name = summoner_name.replace(' ', '')

    summoner = requests.get('https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(summoner_name, api_key))
    summoner = summoner.json()

    total_games = requests.get('https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?season=13&queue=420&endIndex=100&api_key={}'.format(summoner['accountId'], api_key))
    try:
        total_games = int(total_games.json()['totalGames'])
    except KeyError as e:
        print('No Rank Game')

    loop_index = int(total_games / 100)
    last_loop = total_games % 100

    match_id_list = []

    if loop_index > 0:
        for x in range(1, loop_index + 1):
            time.sleep(1)
            match_list = requests.get(
                'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?season=13&startIndex={}&endIndex={}&api_key={}'.format(
                    summoner['accountId'], str(x), str(x), api_key)).json()
            for y in match_list['matches']:
                match_id_list.append(y['gameId'])

    match_id_list = list(set(match_id_list))
    champion_dict = {}

    for match_id in match_id_list:
        time.sleep(1)
        game_result = requests.get(
            'https://kr.api.riotgames.com/lol/match/v4/matches/{}?api_key={}'.format(
                str(match_id), api_key)).json()

        for participantIdentities in game_result['participantIdentities']:
            if participantIdentities['player']['accountId'] == summoner['accountId']:
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

    result_dict = {'summoner': summoner, 'rank_result': champion_dict}

    return result_dict
