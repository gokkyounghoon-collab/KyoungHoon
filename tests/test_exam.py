from gaeun1.db import Question
from gaeun1.exam import select_questions


def make_question(question_id: int, image_url: str | None = None, question_type: str = "multiple_choice") -> Question:
    return Question(
        id=question_id,
        subject="통합과학1",
        author="테스트",
        range="전체",
        difficulty="중",
        content="테스트 내용",
        options=["A", "B", "C"] if question_type == "multiple_choice" else [],
        answer_idx=0,
        image_url=image_url,
        question_type=question_type,
    )


def test_select_questions_multiple_choice_with_image():
    questions = [
        make_question(1, image_url="http://image1.png"),
        make_question(2),
        make_question(3),
    ]

    selected = select_questions(questions, count=2, include_short_answer=False)
    assert len(selected) == 2
    assert any(q.image_url for q in selected)


def test_select_questions_short_answer_includes_at_least_one_short():
    questions = [
        make_question(1, image_url=None, question_type="short_answer"),
        make_question(2, image_url="http://image2.png"),
        make_question(3),
    ]

    selected = select_questions(questions, count=3, include_short_answer=True)
    assert any(q.question_type == "short_answer" for q in selected)


def test_select_questions_zero_count():
    questions = [make_question(1), make_question(2)]
    assert select_questions(questions, count=0) == []
