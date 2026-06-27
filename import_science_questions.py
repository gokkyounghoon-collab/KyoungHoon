import json
import sqlite3

with open('science_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

conn = sqlite3.connect('exam_system.db')
cursor = conn.cursor()

inserted = 0
for item in data:
    subject = item.get('subject', '과학탐구실험')
    question = item.get('question') or item.get('content') or ''
    if not question:
        continue

    # 중복 방지: 동일 subject + question이 이미 있으면 건너뜀
    cursor.execute('SELECT COUNT(*) FROM questions WHERE subject = ? AND content = ?', (subject, question))
    if cursor.fetchone()[0] > 0:
        continue

    choices = item.get('choices') or item.get('options') or []
    answer = item.get('answer')
    if isinstance(answer, int):
        answer_idx = max(0, answer - 1)
    else:
        answer_idx = 0

    question_type = 'multiple_choice' if choices else 'short_answer'
    cursor.execute(
        'INSERT INTO questions (subject, author, range, difficulty, content, options, answer_idx, image_url, question_type, short_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (
            subject,
            item.get('author', '시스템'),
            item.get('range', '전체'),
            item.get('difficulty', '중'),
            question,
            json.dumps(choices, ensure_ascii=False),
            answer_idx,
            item.get('image_url') or item.get('image') or None,
            question_type,
            item.get('short_answer') if question_type == 'short_answer' else None,
        )
    )
    inserted += 1

conn.commit()
conn.close()
print(f'등록된 문제 수: {inserted}')
