import requests
import common
import json


summoner_name ="노란솜"
api_key=common.api_key

# 닉네임을 통해서 소환사 정보를 얻어옴
def summoner_info(name,apikey):
    print(f"{name} 소환사 님의 정보수집")
    summoner_url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={apikey}"
    response = requests.get(summoner_url)
    summonerInfo = response.json()
    return summonerInfo
# 수집한 닉네임에서 puuid를 통해 소환사의match_id를 추출
def get_matchId(puuid,apikey):
    print("게임아이디 수집")
    match_id_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={api_key}"
    m_respnose =requests.get(match_id_url)
    data = m_respnose.json()
    return data
# match_id 의 게임데이터 수집
def get_gameData(match_id,api_key):
    print(f"{match_id} 의 타임라인 및 게임데이터 수집")
    game_data_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    respnose=requests.get(game_data_url)
    gameData = respnose.json()
    return gameData
# match_id 의 타임라인 수집
def get_timeLine(match_id,api_key): 
    timeline_data_url= f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={api_key}"
    respnose=requests.get(timeline_data_url)
    timeLineData = respnose.json()
    return timeLineData



data = summoner_info(summoner_name,api_key)
data = get_matchId(data['puuid'],api_key)
timeline = get_timeLine(data[0],api_key)
print(timeline.keys())
gamedata = get_gameData(data[0],api_key)
print(gamedata.keys())



