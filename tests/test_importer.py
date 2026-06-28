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


def test_convert_import_payload_short_answer_with_question_field():
    payload = ImportQuestion(
        subject="임진왜란의 결과",
        question="임진왜란 이후 일본에서 도쿠가와 이에야스가 실권을 잡고 수립한 막부 정권의 명칭은?",
        short_answer="에도 막부",
        answer="에도 막부",
    )

    converted = convert_import_payload(payload)
    assert converted["subject"] == "임진왜란의 결과"
    assert converted["content"] == "임진왜란 이후 일본에서 도쿠가와 이에야스가 실권을 잡고 수립한 막부 정권의 명칭은?"
    assert converted["question_type"] == "short_answer"
    assert converted["answer_idx"] == 0
    assert converted["short_answer"] == "에도 막부"


def test_convert_import_payload_short_answer_from_answer_only():
    payload = ImportQuestion(
        subject="임진왜란의 결과",
        question="임진왜란 이후 일본에서 도쿠가와 이에야스가 실권을 잡고 수립한 막부 정권의 명칭은?",
        answer="에도 막부",
    )

    converted = convert_import_payload(payload)
    assert converted["question_type"] == "short_answer"
    assert converted["answer_idx"] == 0
    assert converted["short_answer"] == "에도 막부"


def test_convert_import_payload_multiple_choice_without_options_falls_back_to_short_answer():
    payload = ImportQuestion(
        subject="임진왜란의 결과",
        question="임진왜란 이후 일본에서 도쿠가와 이에야스가 실권을 잡고 수립한 막부 정권의 명칭은?",
        answer="에도 막부",
        question_type="multiple_choice",
    )

    converted = convert_import_payload(payload)
    assert converted["question_type"] == "short_answer"
    assert converted["answer_idx"] == 0
    assert converted["short_answer"] == "에도 막부"
