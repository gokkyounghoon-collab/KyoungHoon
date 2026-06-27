import sqlite3
conn = sqlite3.connect('exam_system.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM questions WHERE subject = ?', ('과학탐구실험',))
print('count', cur.fetchone()[0])
cur.execute('SELECT content FROM questions WHERE subject=? LIMIT 3', ('과학탐구실험',))
print(cur.fetchall())
conn.close()
