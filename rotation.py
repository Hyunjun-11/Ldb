import requests
import pandas as pd
import common

# API 키와 챌린저 리그 데이터를 가져올 URL 설정
api_key = common.api
rotations_url = f"https://kr.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={api_key}"

# API 요청을 보내고 응답을 받아옴
response = requests.get(rotations_url)
data = response.json()
print(data)