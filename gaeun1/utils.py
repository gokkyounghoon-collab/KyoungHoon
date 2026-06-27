from typing import Iterable, List, Optional
import socket


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def transform_multiple_choice_content(content: str) -> str:
    content = content.strip()
    if not content:
        return content
    if content.startswith("다음 중") or content.startswith("다음 보기") or content.endswith("?"):
        return content
    return f"다음 중 알맞은 것을 고르시오: {content}"


def transform_short_answer_content(content: str) -> str:
    content = content.strip()
    if not content:
        return content
    if content.endswith("?") or content.startswith("다음"):
        return content
    return f"다음 설명에 해당하는 답을 쓰시오. {content}"


def is_short_answer_question(options: Optional[List[str]], question_type: Optional[str]) -> bool:
    if not options:
        return True
    return (question_type or "multiple_choice") == "short_answer"


def build_question_payload(question: object, transform: bool = False):
    content = question.content or ""
    question_type = "short_answer" if is_short_answer_question(question.options, question.question_type) else "multiple_choice"
    if transform:
        if question_type == "multiple_choice":
            content = transform_multiple_choice_content(content)
        else:
            content = transform_short_answer_content(content)

    return {
        "id": question.id,
        "subject": question.subject,
        "author": question.author,
        "range": question.range,
        "difficulty": question.difficulty,
        "content": content,
        "options": question.options or [],
        "answer_idx": question.answer_idx,
        "image_url": question.image_url,
        "question_type": question_type,
        "short_answer": question.short_answer,
    }


def normalize_question_type(raw: Optional[str]) -> Optional[str]:
    if raw is None:
        return None
    normalized = str(raw).strip().lower()
    if normalized in {"주관식", "short_answer", "short answer", "short-answer"}:
        return "short_answer"
    if normalized in {"객관식", "multiple_choice", "multiple choice", "multiple-choice"}:
        return "multiple_choice"
    return normalized


def normalize_options(options: Optional[Iterable[str]]) -> List[str]:
    if not options:
        return []
    return [str(option).strip() for option in options if str(option).strip()]


def clamp_answer_idx(answer_idx: int, size: int) -> int:
    if size <= 0:
        return 0
    if answer_idx < 0:
        return 0
    if answer_idx >= size:
        return size - 1
    return answer_idx
