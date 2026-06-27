import os
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("GAEUN_DATABASE_URL", "sqlite:///./exam_system.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    author = Column(String, nullable=False)
    range = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    content = Column(String, nullable=False)
    options = Column(JSON, nullable=True)
    answer_idx = Column(Integer, nullable=False, default=0)
    image_url = Column(String, nullable=True)
    question_type = Column(String, nullable=False, default="multiple_choice")
    short_answer = Column(String, nullable=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
