import pandas as pd
import requests
import time
import common
import json

# 정리된 CSV 파일 경로
input_file = '챌린저 데이터.csv'

# CSV 파일 읽기
df = pd.read_csv(input_file)

# 'puuid' 열에서 값 추출, 결측값 제거 또는 변환
puuids = [str(puuid) for puuid in df['puuid'] if pd.notnull(puuid)]

# API 키 설정
api_key = common.api

# 각 puuid에 대한 매치 ID를 저장할 딕셔너리 초기화
matches = {}

# puuid 리스트를 순회하며 매치 ID 요청
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
                print("Match IDs:", match_ids)
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

# matches 딕셔너리를 JSON 파일로 저장
with open('json/matches.json', 'w') as file:
    json.dump(matches, file, ensure_ascii=False, indent=4)

print("매치 ID가 matches.json 파일에 저장되었습니다.")
