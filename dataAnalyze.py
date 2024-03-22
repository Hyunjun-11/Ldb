import common
import json
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
# 데이터베이스 선택
db = client['Ldb']

# 컬렉션 선택
collection = db['itemsInfo']


file_path = "jst.json"

data = common.load_json(file_path)

RED = "\033[31m"  # 빨간색 텍스트
GREEN = "\033[32m"  # 초록색 텍스트
YELLOW = "\033[33m"  # 노란색 텍스트
RESET = "\033[0m"

# print(data.keys())
#
# print(data['metadata'].keys())
# print(data['info'].keys())

info_values = data['info']

def timestamp(event):
    timestamp = event.get('timestamp')  # 밀리초를 분으로 변환
    realTime = timestamp / 60000
    minutes = int(realTime)  # 소수점 이하 버림
    seconds = int((realTime - minutes) * 60)
    return f"{timestamp}===={minutes}분 {seconds}초"  # 시간 문자열 반환

def lane(event):
    
    if event == 1:
        return "[1팀 탑]"
    elif event == 2:
        return "[1팀 정글]"
    elif event == 3:
        return "[1팀 미드]"
    elif event == 4:
        return "[1팀 원딜]"
    elif event == 5:
        return "[1팀 서폿]"
    elif event == 6:
        return "[2팀 탑]"
    elif event == 7:
        return "[2팀 정글]"
    elif event == 8:
        return "[2팀 미드]"
    elif event == 9:
        return "[2팀 원딜]"
    elif event == 10:
        return "[2팀 서폿]"
    else:
        return "Not User"


# 예시 이벤트 유형별 처리 함수
def print_item_purchased(event):
    itemId = str(event.get('itemId'))
    item_info = collection.find_one({"key": itemId})
    item_name = item_info.get('name') if item_info else "알 수 없는 아이템"
    print(timestamp(event),lane(event.get("participantId")), f"아이템 {RED}[{item_name}]{RESET} 구입 ")

def print_skill_level_up(event):
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

def print_champion_kill(event):
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


def print_special_kill(event):
    killType = event.get("killType")
    print(f"{killType}")



def print_champion_levelUp(event):
    print(timestamp(event), lane(event.get("participantId")), "레벨업")

def print_item_destroy(event):
    print(timestamp(event), lane(event.get("participantId")), "아이템 사용")

def print_item_sold(event):
    itemId = str(event.get('itemId'))
    item_info = collection.find_one({"key": itemId})
    item_name = item_info.get('name') if item_info else "알 수 없는 아이템"
    print(timestamp(event), lane(event.get("participantId")), f"{RED}[{item_name}]{RESET} 판매")


def print_item_undo(event):
    print(timestamp(event), lane(event.get("participantId")), "아이템 구매 취소(되돌리기)")

def print_ward_placed(event):
    print(timestamp(event), lane(event.get("creatorId")), "와드 설치")
def print_ward_kill(event):
    print(timestamp(event), lane(event.get("killerId")), "와드 파괴")

def print_turret_plate_destroyed(event):
    TurretLane = event.get("laneType")
    print(timestamp(event),lane(event.get("killerId")), f"{TurretLane} 포탑골드 획득")

def print_elite_monster_kill(event):
    monsterType = event.get("monsterType")
    monsterSubType = event.get("monsterSubType")  # monsterSubType 초기화
    if monsterType == "DRAGON":
        print(f"{timestamp(event)} {lane(event.get('killerId'))} 엘리트몬스터[{monsterSubType}]처치")
    elif monsterType =="BARON":
        print(f"{timestamp(event)} {lane(event.get('killerId'))} 엘리트몬스터[{monsterType}]처치")

def print_building_kill(event):
    towerType=event.get("towerType")
    laneType = event.get("laneType")
    print(f"{common.ConsoleColor.BRIGHT_MAGENTA}{timestamp(event)} {lane(event.get('killerId'))} {laneType} / {towerType}차 터렛 파괴 {common.ConsoleColor.RESET}")

def print_bounty_prstart(event):
   
    print(f"{timestamp(event)} {event.get('teamId')}팀 의 현상금 활성화")



    
    






# 추가 이벤트 유형별 처리 함수...

# 이벤트 유형별 함수 매핑
event_print_functions = {
    'ITEM_PURCHASED': print_item_purchased,
    'SKILL_LEVEL_UP': print_skill_level_up,
    'CHAMPION_KILL': print_champion_kill,
    'CHAMPION_SPECIAL_KILL':print_special_kill,
    'ITEM_DESTROYED': print_item_destroy,
    'LEVEL_UP': print_champion_levelUp,
    'WARD_PLACED':print_ward_placed,
    'TURRET_PLATE_DESTROYED':print_turret_plate_destroyed,
    'WARD_KILL' : print_ward_kill,
    'ITEM_UNDO' :print_item_undo,
    'ELITE_MONSTER_KILL': print_elite_monster_kill,
    'BUILDING_KILL' :print_building_kill,
    'ITEM_SOLD': print_item_sold,
    'OBJECTIVE_BOUNTY_PRESTART' : print_bounty_prstart
    
   
}

# 이벤트 처리
for frame in data['info']['frames']:
    events = frame.get('events')
    for event in events:
        
        event_type = event.get('type')
        if event_type in event_print_functions:
            # 해당 이벤트 유형에 맞는 함수 호출
            event_print_functions[event_type](event)
        else:
            print(f"{common.ConsoleColor.BLUE}처리되지 않은 이벤트 유형: {event_type}{common.ConsoleColor.RESET}")
