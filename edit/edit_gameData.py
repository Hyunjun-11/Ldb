import json

# 파일 이름
file_name = '../json/info.json'

# 파일에서 데이터 읽어오기
with open(file_name, 'r', encoding="utf-8") as file:
    data = json.load(file)

metadata = data.get('metadata', {})
gameInfo = data.get('info', {})
participants = gameInfo.get('participants',{})

# for key, value in metadata.items():
#     print("metadata : " + key)
# for key, value in gameInfo.items():
#     print("gameInfo : " + key)
# participants 리스트의 각 딕셔너리를 순회하면서 키를 출력
# participants 리스트의 각 딕셔너리를 순회하면서 키와 값을 함께 출력
for participant in participants:
    print("Participant Data:")
    for key, value in participant.items():
        print("  Key:", key,"  Value:", value)



