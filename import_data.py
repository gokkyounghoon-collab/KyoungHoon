from gaeun1.db import SessionLocal
from gaeun1.importer import import_questions_from_json


def main() -> None:
    with SessionLocal() as db:
        summary = import_questions_from_json("questions.json", db)

    print(f"등록된 문제: {summary['created']}")
    print(f"건너뛴 문제: {summary['skipped']}")
    if summary["errors"]:
        print("오류 목록:")
        for error in summary["errors"]:
            print(f" - {error}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
