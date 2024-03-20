import requests
import pandas as pd
import common

# API 키와 챌린저 리그 데이터를 가져올 URL 설정
api_key = common.api
challenger_url = f"https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}"

# API 요청을 보내고 응답을 받아옴
response = requests.get(challenger_url)
data = response.json()

# 데이터프레임 생성
league_df = pd.DataFrame(data['entries'])

# 필요한 열만 선택하고 데이터 타입 변환
league_df['leaguePoints'] = league_df['leaguePoints'].astype(int)
league_df['wins'] = league_df['wins'].astype(int)
league_df['losses'] = league_df['losses'].astype(int)

# 특정 boolean 값을 가지는 열들을 정수형으로 변환
league_df['veteran'] = league_df['veteran'].astype(int)
league_df['inactive'] = league_df['inactive'].astype(int)
league_df['freshBlood'] = league_df['freshBlood'].astype(int)
league_df['hotStreak'] = league_df['hotStreak'].astype(int)

# 결과 확인
print(league_df.info())

# 결과를 CSV 파일로 저장
league_df.to_csv('챌린저 데이터.csv', index=False, encoding='utf-8')
