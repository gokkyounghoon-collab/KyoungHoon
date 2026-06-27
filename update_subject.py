import json

# 파일 읽기
with open('science_experiment_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# subject 변경
for q in data:
    q['subject'] = '과학탐구실험'

# 파일 쓰기
with open('science_experiment_questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("과목 변경 완료")