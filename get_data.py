import pymongo

client = pymongo.MongoClient('localhost', 27017)

db = client["Ldb"]

print(db.list_collection_names())



collection = db["inGameData"]
document_count = collection.count_documents({})
print((document_count))

summoner_name="노란솜"





#소환사 이름으로 검색하기
summoner_name_pipeline = [
    {"$unwind": "$info.participants"},  # 배열을 풀어서 개별 문서로 만듦
    {"$match": {"info.participants.summonerName": summoner_name}},  # 필터링 조건을 지정
    {"$group": {"_id": "$metadata.matchId", "participants": {"$push": "$info.participants"}}}  # matchId를 기준으로 그룹화하여 participants 필드로 모으기
]


total_damage_pipeline = [
    {"$unwind": "$info.participants"},
    {"$group": {
        "_id": "$metadata.matchId",
        "participants": {
            "$push": {
                "championName": "$info.participants.championName",
                "physicalDamageDealtToChampions": "$info.participants.physicalDamageDealtToChampions"
            }
        }
    }}
]

ex_pipeline = [
    {"$unwind": "$info.participants"},
    {"$match": {"info.participants.championName": "Caitlyn"}},
    {"$group": {
        "_id": "$metadata.matchId",
        "participants": {
            "$push": {
                "championName": "$info.participants.championName",
                "physicalDamageDealtToChampions": "$info.participants.physicalDamageDealtToChampions"
            }
        }
    }}
    # matchId를 기준으로 그룹화하여 participants 필드로 모으기
]
match=[
    {"$match": {"metadata.matchId":"KR_6991821768"}}

]
win_pipeline=[
    {"$unwind": "$info.participants"},
    {"$match": {"info.participants.teamPosition":"MIDDLE"}},
    {"$group":{
        "_id": "$metadata.matchId",
        "participants": {
            "$push":{
                "championName": "$info.participants.championName",
                "win":"$info.participants.win"
            }
        }
    }}
]


documents_with_summoner = collection.aggregate(win_pipeline)
for document in documents_with_summoner:
    print(document)

