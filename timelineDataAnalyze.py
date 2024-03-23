import common
import json
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
# 데이터베이스 선택
db = client['Ldb']

# 컬렉션 선택
#아이템 정보 불러오기
collection = db['itemsInfo']
file_path = "jst.json"

data = common.load_json(file_path)

RED = "\033[31m"  # 빨간색 텍스트
GREEN = "\033[32m"  # 초록색 텍스트
YELLOW = "\033[33m"  # 노란색 텍스트
RESET = "\033[0m"

#타임라인 분 초 로 변환(밀리초)
def timestamp(event):
    timestamp = event.get('timestamp')  # 밀리초를 분으로 변환
    realTime = timestamp / 60000
    minutes = int(realTime)  # 소수점 이하 버림
    seconds = int((realTime - minutes) * 60)
    return f"{timestamp} ==={minutes}분 {seconds}초 == "  # 시간 문자열 반환
#챔피언 아이디별로 라인
def lane(event):
    if event == 1:
        return "[블루팀 탑]"
    elif event == 2:
        return "[블루팀 정글]"
    elif event == 3:
        return "[블루팀 미드]"
    elif event == 4:
        return "[블루팀 원딜]"
    elif event == 5:
        return "[블루팀 서폿]"
    elif event == 6:
        return "[레드팀 탑]"
    elif event == 7:
        return "[레드팀 정글]"
    elif event == 8:
        return "[레드팀 미드]"
    elif event == 9:
        return "[레드팀 원딜]"
    elif event == 10:
        return "[레드팀 서폿]"
    else:
        return "Not User"

# 아이템 구입
def item_purchased(event):
    itemId = str(event.get('itemId'))
    item_info = collection.find_one({"key": itemId})
    item_name = item_info.get('name') if item_info else "알 수 없는 아이템"
    print(timestamp(event),lane(event.get("participantId")), f"아이템 {RED}[{item_name}]{RESET} 구입 ")
# 아이템 사용
def item_destroy(event):
    print(timestamp(event), lane(event.get("participantId")), "아이템 사용")
# 아이템 판매
def item_sold(event):
    itemId = str(event.get('itemId'))
    item_info = collection.find_one({"key": itemId})
    item_name = item_info.get('name') if item_info else "알 수 없는 아이템"
    print(timestamp(event), lane(event.get("participantId")), f"{RED}[{item_name}]{RESET} 판매")
# 아이템 되돌리기
def item_undo(event):
    print(timestamp(event), lane(event.get("participantId")), "아이템 구매 취소(되돌리기)")

# 스킬찍은거
def skill_level_up(event):
    skill_up =event.get("skillSlot")
    if skill_up == 1:
        skill_up = "q"
    elif skill_up == 2:
        skill_up = "w"
    elif skill_up == 3:
        skill_up = "e"
    elif skill_up == 4:
        skill_up = "r"
    print(timestamp(event), lane(event.get("participantId")), {skill_up},"선택")

# 킬
def champion_kill(event):
    killer_position = lane(event.get('killerId'))
    victim_position = lane(event.get('victimId'))
    
    # 어시스트 참가자 ID 리스트
    assisting_ids = event.get('assistingParticipantIds', [])
    
    # 어시스트 참가자 포지션 문자열 리스트 생성
    assisting_positions = [lane(id) for id in assisting_ids]
    
    # 어시스트 참가자 포지션 문자열 리스트를 하나의 문자열로 합치기
    assisting_positions_str = ", ".join(assisting_positions)
    #획득골드
    bounty =event.get("bounty")
    #현상금
    shutdownBounty =event.get("shutdownBounty")
    
    # 최종 결과 출력
    print(f"{YELLOW}{timestamp(event)} 챔피언 처치: 처치자 {killer_position}, 희생자 {victim_position}, 어시스트: {assisting_positions_str}, 획득 골드{bounty}{RESET}")
# 스페셜 킬(퍼스트 블러드)
def special_kill(event):
    killType = event.get("killType")
    print(f"{killType}")
# 챔피언 레벨업
def champion_levelUp(event):
    print(timestamp(event), lane(event.get("participantId")), "레벨업")

# 와드 설치
def ward_placed(event):
    print(timestamp(event), lane(event.get("creatorId")), "와드 설치")
#와드 파괴
def ward_kill(event):
    print(timestamp(event), lane(event.get("killerId")), "와드 파괴")
#포탑 골드 획득
def turret_plate_destroyed(event):
    TurretLane = event.get("laneType")
    print(timestamp(event),lane(event.get("killerId")), f"{TurretLane} 포탑골드 획득")
#포탑 파괴
def building_kill(event):
    towerType=event.get("towerType")
    laneType = event.get("laneType")
    print(f"{common.ConsoleColor.BRIGHT_MAGENTA}{timestamp(event)} {lane(event.get('killerId'))} {laneType} / {towerType}차 터렛 파괴 {common.ConsoleColor.RESET}")
#현상금 활성화 시간표시
def bounty_prstart(event):
   
    print(f"{timestamp(event)} {event.get('teamId')}팀 의 현상금 활성화")
# 드래곤or 바론
def elite_monster_kill(event):
    monsterType = event.get("monsterType")
    monsterSubType = event.get("monsterSubType")  # monsterSubType 초기화
    if monsterType == "DRAGON":
        print(f"{timestamp(event)} {lane(event.get('killerId'))} 엘리트몬스터[{monsterSubType}] 드래곤 처치")
    elif monsterType =="BARON_NASHOR":
        print(f"{timestamp(event)} {lane(event.get('killerId'))} 엘리트몬스터 [바론] 처치")

# 이벤트 유형별 함수 매핑
event_print_functions = {
    'ITEM_PURCHASED': item_purchased,
    'SKILL_LEVEL_UP': skill_level_up,
    'CHAMPION_KILL': champion_kill,
    'CHAMPION_SPECIAL_KILL':special_kill,
    'ITEM_DESTROYED': item_destroy,
    'LEVEL_UP': champion_levelUp,
    'WARD_PLACED':ward_placed,
    'TURRET_PLATE_DESTROYED':turret_plate_destroyed,
    'WARD_KILL' : ward_kill,
    'ITEM_UNDO' :item_undo,
    'ELITE_MONSTER_KILL': elite_monster_kill,
    'BUILDING_KILL' :building_kill,
    'ITEM_SOLD': item_sold,
    'OBJECTIVE_BOUNTY_PRESTART' : bounty_prstart
    
   
}

# 이벤트 처리
for frame in data['info']['frames']:
    events = frame.get('events')
    for event in events:
        event_type = event.get('type')
        if event_type in event_print_functions:
            event_print_functions[event_type](event)
        else:
            print(f"{common.ConsoleColor.BLUE}처리되지 않은 이벤트 유형: {event_type}{common.ConsoleColor.RESET}")
