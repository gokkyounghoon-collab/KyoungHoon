from gaeun1.scraper import generate_science_questions_json


def main() -> None:
    total = generate_science_questions_json("science_questions.json")
    print(f"완료: science_questions.json 생성됨 ({total}개)")


if __name__ == "__main__":
    main()
