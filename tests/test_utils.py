import pytest
from gaeun1.utils import clamp_answer_idx, normalize_options, normalize_question_type


def test_normalize_options_none():
    assert normalize_options(None) == []


def test_normalize_options_trim_and_filter():
    assert normalize_options([" a ", "", "b"]) == ["a", "b"]


def test_normalize_question_type_multiple_choice():
    assert normalize_question_type("객관식") == "multiple_choice"
    assert normalize_question_type("multiple choice") == "multiple_choice"


def test_normalize_question_type_short_answer():
    assert normalize_question_type("주관식") == "short_answer"
    assert normalize_question_type("short-answer") == "short_answer"


def test_clamp_answer_idx_bounds():
    assert clamp_answer_idx(-1, 4) == 0
    assert clamp_answer_idx(5, 4) == 3
    assert clamp_answer_idx(2, 4) == 2
