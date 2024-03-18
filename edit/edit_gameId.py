import json

# 파일 이름
file_name = '../json/matches.json'

# 파일에서 데이터 읽어오기
with open(file_name, 'r') as file:
    data = json.load(file)

# 중복된 matchId 제거하여 유일한 값만 추출
# set은 중복데이터가 들어갈 수 없다.
unique_match_ids = set()
for value_list in data.values():
    unique_match_ids.update(value_list)

# 유일한 matchId 출력
print("유일한 matchId:")
for match_id in unique_match_ids:
    print(match_id)
