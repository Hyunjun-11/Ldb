import common
import json

file_path = "jst.json"
data = common.load_json(file_path)

print(data.keys())

print(data['metadata'].keys())
print(data['info'].keys())

info_values = data['info']

for key, value in info_values.items():
    print(f"{key} : {type(value)}")


for frame in data['info']['frames'][:10]:
    events = frame.get('events')
    for event_data in events:  # 처음 10개 이벤트 데이터만을 순회
        timestamp = event_data.get('timestamp')  # 밀리초를 분으로 변환
        realTime = timestamp/60000
        minutes = int(realTime)  # 소수점 이하 버림
        seconds = int((realTime - minutes) * 60)  # 소수점 이하 초로 변환
        type = event_data.get('type')
        itemId = event_data.get('itemId')
        participantId = event_data.get('participantId')
        skillSlot = event_data.get('skillSlot')
        wardType = event_data.get('wardType')
        creatorId = event_data.get('creatorId')
        levelUpType = event_data.get('levelUpType')
        level = event_data.get('level')
        killerId = event_data.get('killerId')
        print(
            # f"{minutes}분 {seconds}초",
              timestamp,
            #   itemId,
            #   type,
            #   participantId,
            #   skillSlot,
            #   wardType,
            #   creatorId,
            #   levelUpType,
            #   level,
            #   killerId,
              )
