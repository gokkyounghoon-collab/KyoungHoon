import pytest
from gaeun1.importer import convert_import_payload
from gaeun1.schemas import ImportQuestion


def test_convert_import_payload_multiple_choice():
    payload = ImportQuestion(
        subject="통합과학1",
        author="저자",
        range="전체",
        difficulty="중",
        content="문제 내용",
        options=["A", "B", "C"],
        answer=2,
    )

    converted = convert_import_payload(payload)
    assert converted["subject"] == "통합과학1"
    assert converted["question_type"] == "multiple_choice"
    assert converted["answer_idx"] == 2
    assert converted["options"] == ["A", "B", "C"]


def test_convert_import_payload_short_answer():
    payload = ImportQuestion(
        subject="과학탐구실험",
        content="다음 설명에 해당하는 답은?",
        type="short_answer",
        answer="물질",
    )

    converted = convert_import_payload(payload)
    assert converted["question_type"] == "short_answer"
    assert converted["answer_idx"] == 0
    assert converted["short_answer"] == "물질"


def test_convert_import_payload_invalid_short_answer():
    payload = ImportQuestion(
        subject="과학탐구실험",
        content="서술형 문제",
        type="short_answer",
    )

    with pytest.raises(ValueError):
        convert_import_payload(payload)
