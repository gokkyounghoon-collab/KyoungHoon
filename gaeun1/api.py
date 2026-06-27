from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from .db import init_db, get_db, Question
from .exam import build_question_payloads, select_questions
from .schemas import Question as QuestionSchema, QuestionExportPayload, ImportQuestion
from .utils import get_local_ip, is_short_answer_question


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="High School Exam System", lifespan=lifespan)

if not os.path.exists("images"):
    os.makedirs("images")
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/server-info")
def get_server_info() -> dict:
    return {"url": f"http://{get_local_ip()}:8000"}


@app.get("/generate-exam/{subject}", response_model=list[QuestionSchema])
def generate_exam(
    subject: str,
    author: str | None = None,
    range: list[str] | None = Query(None),
    difficulty: str | None = None,
    count: int = 10,
    transform: bool = False,
    include_short_answer: bool = False,
    db: Session = Depends(get_db),
) -> list[dict]:
    query = db.query(Question).filter(Question.subject == subject)
    if author:
        query = query.filter(Question.author == author)
    if range:
        query = query.filter(Question.range.in_(range))
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if not include_short_answer:
        query = query.filter(Question.question_type == "multiple_choice")

    questions = query.all()
    if not questions:
        return []

    questions = select_questions(questions, count=count, include_short_answer=include_short_answer)
    return build_question_payloads(questions, transform)


@app.get("/export-questions", response_model=QuestionExportPayload)
def export_questions(db: Session = Depends(get_db)) -> QuestionExportPayload:
    questions = db.query(Question).all()
    multiple_choice = [q for q in questions if q.question_type == "multiple_choice"]
    short_answer = [q for q in questions if q.question_type == "short_answer"]
    return QuestionExportPayload(multiple_choice=multiple_choice, short_answer=short_answer)


@app.post("/import-questions")
def import_questions(questions: list[ImportQuestion], db: Session = Depends(get_db)) -> dict:
    from .importer import convert_import_payload

    db_questions = []
    for q in questions:
        try:
            converted = convert_import_payload(q)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        db_questions.append(Question(**converted))

    if db_questions:
        db.add_all(db_questions)
        db.commit()
    return {"message": f"{len(db_questions)}개의 문제가 성공적으로 등록되었습니다."}


@app.delete("/delete-all-questions")
def delete_all_questions(db: Session = Depends(get_db)) -> dict:
    count = db.query(Question).delete()
    db.commit()
    return {"message": f"{count}개의 문제가 삭제되었습니다."}


@app.post("/report-error")
def report_error(question_id: int, db: Session = Depends(get_db)) -> dict:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": f"문제 {question_id}번이 오답 노트에 추가되었습니다."}


@app.get("/")
def read_root() -> FileResponse:
    index_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)
