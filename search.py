import requests
import pandas as pd
import time
import common

# API 키와 챌린저 리그 데이터를 가져올 URL 설정
api_key = common.api
challenger_url = f"https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}"

# 챌린저 데이터 호출
response = requests.get(challenger_url)
league_df = pd.DataFrame(response.json())

# 'entries' 열의 데이터를 확장하여 DataFrame에 추가
league_entries_df = pd.DataFrame(league_df['entries'].values.tolist())
league_df = pd.concat([league_df, league_entries_df], axis=1)

# 각 행의 'summonerName'을 사용하여 소환사의 계정 ID를 가져옴
for index, row in league_df.iterrows():
    try:
        sohwan = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{row['summonerName']}?api_key={api_key}"
        r = requests.get(sohwan)
        
        while r.status_code == 429:  # API 요청 제한에 도달한 경우 대기
            time.sleep(5)
            r = requests.get(sohwan)
            
        puuid = r.json().get('puuid')
        if puuid:  # puuid가 존재하는 경우에만 값을 업데이트
            league_df.at[index, 'puuid'] = puuid
    except Exception as e:
        print(f"An error occurred for summoner: {row['summonerName']}, Error: {e}")

# 챌린저 데이터를 CSV 파일로 저장
league_df.to_csv('챌린저 데이터.csv', index=False, encoding='utf-8')
