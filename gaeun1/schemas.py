from __future__ import annotations

from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class QuestionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    author: str
    range: str
    difficulty: str
    content: str
    options: List[str] = Field(default_factory=list)
    answer_idx: int = 0
    image_url: Optional[str] = None
    question_type: str = "multiple_choice"
    short_answer: Optional[str] = None


class Question(QuestionBase):
    id: Optional[int] = None


class QuestionExportPayload(BaseModel):
    multiple_choice: List[Question] = Field(default_factory=list)
    short_answer: List[Question] = Field(default_factory=list)


class ImportQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: Optional[str] = None
    author: Optional[str] = None
    range: Optional[str] = None
    difficulty: Optional[str] = None
    content: Optional[str] = None
    question: Optional[str] = None
    options: Optional[List[str]] = None
    choices: Optional[List[str]] = None
    answer_idx: Optional[int] = None
    answer: Optional[Union[int, str]] = None
    question_type: Optional[str] = None
    type: Optional[str] = None
    short_answer: Optional[str] = None
    image_url: Optional[str] = None
    image: Optional[str] = None

    def normalized_question_type(self) -> Optional[str]:
        raw = self.question_type or self.type
        if raw is None:
            return None
        normalized = str(raw).strip().lower()
        if normalized in {"주관식", "short_answer", "short answer", "short-answer"}:
            return "short_answer"
        if normalized in {"객관식", "multiple_choice", "multiple choice", "multiple-choice"}:
            return "multiple_choice"
        return normalized
