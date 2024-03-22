import os
import json
import pymongo

# MongoDB 서버에 연결
client = pymongo.MongoClient("mongodb://localhost:27017/")  # MongoDB가 실행 중인 호스트와 포트

# 데이터베이스 선택
db = client['Ldb']

# 컬렉션 선택
collection = db['itemsInfo']

championNum = "챔피언 데이터/14.5.1/data/ko_KR/champion"

# 디렉토리 안에 있는 모든 파일 목록 가져오기
file_list = os.listdir(championNum)

# JSON 파일만 필터링
json_files = [file for file in file_list if file.endswith('.json')]

# 각 JSON 파일에서 "name" 필드 추출하기
for json_file in json_files:
    with open(os.path.join(championNum, json_file), 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data["data"], dict):  # 데이터가 딕셔너리인 경우에만 처리
            for champion, champion_data in data["data"].items():
                champion_id = champion_data["id"]
                champion_name = champion_data["name"]
                champion_key = champion_data["key"]
                print(champion_id, champion_name, champion_key)
#                 # MongoDB에 삽입
#                 collection.insert_one({
#                     "name": champion_name,
#                     "key": champion_key,
#                     "path": f"{champion_id}.png"
#                 })




file_path = "챔피언 데이터/14.5.1/data/ko_KR/item.json"

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# "data" 딕셔너리에서 각 아이템의 ID와 이름을 가져와 출력합니다.
for item_id, item_info in data["data"].items():
    item_name = item_info["name"]
    colloq = item_info["colloq"]
    print("아이템 ID:", item_id, "/  아이템 이름:", item_name)
    # MongoDB에 삽입
    # collection.insert_one({
    #     "name": item_name,
    #     "key": item_id,
    #     "path": f"{item_id}.png"
    # })
