import requests
import pandas as pd
import time
import json
import common  # common.py 파일에서 API 키를 가져옴

# API 키 설정


def get_challenger_data(api_key):
    challenger_url = f"https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}"
    response = requests.get(challenger_url)

    if response.status_code == 200:
        league_df = pd.DataFrame(response.json())
        league_entries_df = pd.DataFrame(league_df['entries'].values.tolist())
        league_df = pd.concat([league_df, league_entries_df], axis=1)
        return league_df
    else:
        print("Failed to retrieve challenger data.")
        return None

# 각 소환사의 puuid 가져오기
def get_puuids(api_key, league_df):
    puuids = []  # puuid들을 담을 빈 리스트

    for index, row in league_df.iterrows():
        if index >= 10:  # 20번째 인덱스에 도달하면 반복 중단
            break
        print(row['summonerName'])
        summoner_url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{row['summonerName']}?api_key={api_key}"
        response = requests.get(summoner_url)

        while response.status_code == 429:  # API 요청 제한에 도달한 경우 대기
            time.sleep(5)
            response = requests.get(summoner_url)
        if response.status_code == 200:
            puuid = response.json().get('puuid')
            if puuid:
                puuids.append(puuid)  # puuid를 리스트에 추가
                print(puuid)
            else:
                print(f"Error fetching puuid for {row['summonerName']}: No puuid found")
        else:
            print(f"Error fetching puuid for {row['summonerName']}: {response.status_code}")

    return puuids


def get_match_ids(api_key, puuids):
    matches = {}

    for puuid in puuids:
        print(puuid + "시도")
        success = False
        attempts = 0

        while not success and attempts < 5:  # 최대 5번 재시도
            try:
                # API URL 구성, 동적으로 puuid 사용
                matches_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={api_key}"
                response = requests.get(matches_url)
                attempts += 1

                if response.status_code == 200:
                    match_ids = response.json()
                    # print("Match IDs:", match_ids)
                    matches[puuid] = match_ids
                    success = True
                elif response.status_code == 429:
                    print(f"Rate limit exceeded for puuid {puuid}. Waiting to retry...")
                    time.sleep((attempts * 10))  # 점차적으로 대기 시간 증가
                else:
                    print(f"Failed to fetch matches for puuid {puuid}: {response.status_code}")
                    break  # 비정상 응답인 경우 재시도 중단
            except Exception as e:
                print(f"An error occurred while fetching matches for puuid {puuid}: {e}")
                break  # 예외 발생 시 재시도 중단
    return matches






