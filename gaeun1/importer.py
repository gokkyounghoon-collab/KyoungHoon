import json
import logging
from typing import Any, Iterable, List
from sqlalchemy.orm import Session
from .db import Question
from .schemas import ImportQuestion
from .utils import clamp_answer_idx, normalize_options, normalize_question_type

logger = logging.getLogger(__name__)


def sanitize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def load_questions_from_json(path: str) -> List[dict]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"JSON 파일을 찾을 수 없습니다: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 파싱 오류: {exc}") from exc

    if isinstance(data, dict) and "questions" in data:
        return data["questions"]
    if isinstance(data, list):
        return data
    raise ValueError("JSON 파일에 유효한 질문 목록이 없습니다.")


def convert_import_payload(payload: ImportQuestion) -> dict:
    subject = sanitize_text(payload.subject) or "통합과학1"
    content = sanitize_text(payload.content or payload.question)
    options = normalize_options(payload.options or payload.choices)
    question_type = normalize_question_type(payload.question_type or payload.type) or (
        "short_answer" if not options else "multiple_choice"
    )

    short_answer = sanitize_text(payload.short_answer)
    answer_idx = payload.answer_idx
    answer_value = payload.answer

    if question_type == "multiple_choice" and not options and answer_value is not None:
        question_type = "short_answer"

    if question_type == "short_answer":
        if not short_answer and answer_value is not None:
            short_answer = sanitize_text(answer_value)
        if not short_answer:
            raise ValueError("주관식 문제는 short_answer 또는 answer 필드를 포함해야 합니다.")
        answer_idx = 0
    else:
        if not options:
            raise ValueError("객관식 문제는 options 필드를 포함해야 합니다.")
        if answer_idx is None:
            if isinstance(answer_value, int):
                answer_idx = answer_value
            elif isinstance(answer_value, str):
                stripped = answer_value.strip()
                if stripped.isdigit():
                    answer_idx = int(stripped) - 1
                elif stripped in options:
                    answer_idx = options.index(stripped)
                else:
                    answer_idx = 0
            else:
                answer_idx = 0
        answer_idx = clamp_answer_idx(answer_idx, len(options))

    return {
        "subject": subject,
        "author": sanitize_text(payload.author) or "미정",
        "range": sanitize_text(payload.range) or "전체",
        "difficulty": sanitize_text(payload.difficulty) or "중",
        "content": content,
        "options": options,
        "answer_idx": answer_idx,
        "image_url": sanitize_text(payload.image_url or payload.image) or None,
        "question_type": question_type,
        "short_answer": short_answer or None,
    }


def import_questions_from_json(path: str, db: Session) -> dict:
    raw_questions = load_questions_from_json(path)
    questions = []
    errors: List[str] = []
    skipped = 0

    for index, raw in enumerate(raw_questions, start=1):
        try:
            payload = ImportQuestion(**raw)
            converted = convert_import_payload(payload)
            if not converted["subject"] or not converted["content"]:
                skipped += 1
                errors.append(f"{index}: subject/content 누락")
                continue
            questions.append(Question(**converted))
        except Exception as exc:
            skipped += 1
            message = f"{index}: {exc}"
            logger.warning(message)
            errors.append(message)

    if questions:
        db.add_all(questions)
        db.commit()

    return {
        "created": len(questions),
        "skipped": skipped,
        "errors": errors,
    }


def clear_all_questions(db: Session) -> int:
    count = db.query(Question).delete()
    db.commit()
    return count
