import json
import sqlite3

with open('science_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

conn = sqlite3.connect('exam_system.db')
cur = conn.cursor()
updated = 0
inserted = 0

for item in data:
    subject = item.get('subject', '과학탐구실험')
    content = item.get('question') or item.get('content') or ''
    if not content:
        continue
    choices = item.get('choices') or item.get('options') or []
    answer = item.get('answer')
    answer_idx = 0
    if isinstance(answer, int):
        answer_idx = max(0, answer - 1)
    elif isinstance(answer, str) and answer.isdigit():
        answer_idx = max(0, int(answer) - 1)

    question_type = 'multiple_choice' if choices else 'short_answer'
    options_json = json.dumps(choices, ensure_ascii=False)

    cur.execute('SELECT id, options, question_type FROM questions WHERE subject = ? AND content = ?', (subject, content))
    row = cur.fetchone()
    if row:
        qid, existing_options, existing_qtype = row
        if existing_options != options_json or existing_qtype != question_type:
            cur.execute(
                'UPDATE questions SET options = ?, question_type = ?, answer_idx = ? WHERE id = ?',
                (options_json, question_type, answer_idx, qid)
            )
            updated += 1
    else:
        cur.execute(
            'INSERT INTO questions (subject, author, range, difficulty, content, options, answer_idx, image_url, question_type, short_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                subject,
                item.get('author', '시스템'),
                item.get('range', '전체'),
                item.get('difficulty', '중'),
                content,
                options_json,
                answer_idx,
                item.get('image_url') or item.get('image') or None,
                question_type,
                None,
            )
        )
        inserted += 1

conn.commit()
conn.close()
print(f'Updated: {updated}, Inserted: {inserted}')
