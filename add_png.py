import json

# JSON 파일 로드
with open('science_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 각 항목의 image 필드에 .png 추가
for item in data:
    if item['image'] and isinstance(item['image'], str):
        item['image'] += '.png'

# 수정된 JSON 저장
with open('science_questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("이미지 URL에 .png 추가 완료")