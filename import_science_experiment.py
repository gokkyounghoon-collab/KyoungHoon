import json
import sqlite3

# JSON 파일 읽기
with open('science_experiment_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 데이터베이스 연결
conn = sqlite3.connect('exam_system.db')
cursor = conn.cursor()

# 새 데이터 삽입 (기존 데이터 유지)
for q in data:
    cursor.execute('''
        INSERT INTO questions (subject, author, range, difficulty, content, options, answer_idx, image_url, question_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        q.get('subject', '과학탐구실험'),
        q.get('author', '시스템'),
        q.get('range', '전체'),
        q.get('difficulty', '중'),
        q.get('question', ''),
        json.dumps(q.get('choices', [])),
        q.get('answer', 1) - 1,  # 1-based to 0-based
        q.get('image', ''),
        'multiple_choice' if q.get('choices') else 'short_answer'
    ))

conn.commit()
conn.close()

print(f'{len(data)}개 문제 등록 완료')