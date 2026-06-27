# 프로젝트 리팩토링 시작

목표: 패키지화 및 스타일 정리(Black, isort, flake8) 적용

빠른 시작

1. 가상환경 생성 및 활성화 (PowerShell)

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

2. 의존성 설치

```powershell
pip install -r requirements.txt
```

3. 코드 포맷/정리

```powershell
pip install black isort flake8
black .
isort .
flake8 .
```

4. 실행

```powershell
python app.py
# 또는
python -m gaeun1
```

5. 데이터 로드

```powershell
python import_data.py
```

6. 이미지 질문 생성

```powershell
setx GAEUN_CHROMEDRIVER_PATH "C:\path\to\chromedriver.exe"
python images_crwler.py
```

`GAEUN_CHROMEDRIVER_PATH` 환경 변수를 설정하면 `selenium`이 올바른 ChromeDriver를 찾도록 도와줍니다.

7. 테스트 실행

```powershell
pytest
```

8. 데이터베이스 마이그레이션

```powershell
alembic upgrade head
```

새 마이그레이션을 생성하려면:

```powershell
alembic revision --autogenerate -m "migration message"
```

또는 Python 스크립트로 실행하려면:

```powershell
python migrate_db.py upgrade
```

9. 데이터베이스 초기화

```powershell
python reset_db.py
```

다음 작업 제안
+- `app.py`, `import_data.py`, `images_crwler.py`를 `gaeun1` 패키지로 래핑
- 타입 힌트 추가 및 함수 단위로 분리
- `pytest` 기반 유닛 테스트 추가
