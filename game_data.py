import requests
import pandas as pd
import pymongo

import common


def get_game_data(api_key,match_id):
    game_dataUrl = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    response = requests.get(game_dataUrl)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"failed to game data for {match_id}", match_id)
        return None


def save_to_mongo(game_data, collection_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["your_database_name"]
    collection = db[collection_name]
    collection.insert_one(game_data)
    print("MongoDB저장완료")

api_key = common.api_key
match_id = "KR_6986916109"

# 게임 데이터 가져오기
game_data = get_game_data(api_key, match_id)
print(game_data)


if game_data:
    # MongoDB에 데이터 저장
    save_to_mongo(game_data, "test_data")  # 여기에 사용할 컬렉션 이름을 입력하세요.
    print("저장완료")
