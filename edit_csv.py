import csv

# 기존 CSV 파일 경로
input_file = '챌린저 데이터.csv'

# 새로 작성될 CSV 파일 경로
output_file = '정리된데이터.csv'

# 삭제하고자 하는 컬럼의 헤더 이름들
headers_to_delete = ['leagueId', 'name']  # 삭제하고자 하는 모든 헤더 이름을 포함하는 리스트입니다.

# CSV 파일 읽기
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)  # 헤더 부분을 가져옵니다.

    # 변경된 헤더 생성
    new_header = [col for col in header if col not in headers_to_delete]

    # 변경된 행들 생성
    new_rows = []
    column_indices_to_delete = [header.index(header_name) for header_name in headers_to_delete]
    for row in reader:
        new_row = [col for i, col in enumerate(row) if i not in column_indices_to_delete]
        new_rows.append(new_row)

# 변경된 정보가 적용된 CSV 파일 쓰기
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(new_header)  # 변경된 헤더를 쓰고,
    writer.writerows(new_rows)  # 변경된 행들을 씁니다.

print("CSV 파일이 성공적으로 수정되었습니다.")
