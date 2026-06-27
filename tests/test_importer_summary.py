from gaeun1.importer import import_questions_from_json, load_questions_from_json
from gaeun1.schemas import ImportQuestion
from gaeun1.db import SessionLocal
import json


def test_import_questions_summary(tmp_path):
    data = [
        {"subject": "통합과학1", "content": "문제1", "options": ["A", "B"], "answer": 1},
        {"subject": "", "content": "", "options": ["A"], "answer": 1},
    ]
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    with SessionLocal() as db:
        summary = import_questions_from_json(str(path), db)

    assert summary["created"] == 1
    assert summary["skipped"] == 1
    assert len(summary["errors"]) == 1
