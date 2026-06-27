from __future__ import annotations

import random
from typing import Iterable, List
from .db import Question
from .utils import build_question_payload, is_short_answer_question


def _choose_image_question(questions: list[Question]) -> Question | None:
    image_questions = [question for question in questions if question.image_url]
    return random.choice(image_questions) if image_questions else None


def select_questions(
    questions: list[Question], count: int, include_short_answer: bool = False
) -> list[Question]:
    if not questions or count <= 0:
        return []

    if include_short_answer:
        short_questions = [q for q in questions if is_short_answer_question(q.options, q.question_type)]
        required_short = min(len(short_questions), max(1, (count + 4) // 5))
        selected: list[Question] = []

        image_question = _choose_image_question(questions)
        if image_question is not None and len(selected) < count:
            selected.append(image_question)
            if image_question.question_type == "short_answer" and required_short > 0:
                required_short -= 1
            questions = [q for q in questions if q.id != image_question.id]
            short_questions = [q for q in short_questions if q.id != image_question.id]

        if required_short > 0 and short_questions:
            selected.extend(short_questions[:required_short])

        remaining = count - len(selected)
        remaining_pool = [q for q in questions if q.id not in {item.id for item in selected}]
        if remaining > 0 and remaining_pool:
            selected.extend(random.sample(remaining_pool, min(len(remaining_pool), remaining)))

        random.shuffle(selected)
        return selected

    if count < len(questions):
        image_question = _choose_image_question(questions)
        if image_question is not None:
            selected = [image_question]
            pool = [q for q in questions if q.id != image_question.id]
            if pool:
                selected.extend(random.sample(pool, min(len(pool), count - 1)))
            random.shuffle(selected)
            return selected
        return random.sample(questions, count)

    random.shuffle(questions)
    return questions


def build_question_payloads(questions: Iterable[Question], transform: bool = False) -> list[dict]:
    return [build_question_payload(question, transform) for question in questions]
