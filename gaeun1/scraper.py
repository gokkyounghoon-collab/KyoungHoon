import json
import logging
import os
from typing import Optional
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

DEFAULT_QUESTIONS = [
    ("세포 구조", "다음 그림은 세포의 구조이다. 핵의 역할로 옳은 것은?", ["단백질 합성", "에너지 생성", "유전 정보 저장", "물질 이동"], 3),
    ("물질 상태 변화", "다음 그림은 상태 변화를 나타낸 것이다. A→B 변화는?", ["융해", "기화", "응고", "승화"], 1),
    ("태양계", "다음은 태양계이다. 지구의 위치는?", ["1번째", "2번째", "3번째", "4번째"], 3),
    ("힘 작용", "다음 그림에서 물체가 정지하는 조건은?", ["힘=0", "힘 일정", "속도 증가", "질량 증가"], 1),
    ("DNA 구조", "다음은 DNA 구조이다. 염기 결합은?", ["A-T, G-C", "A-G, T-C", "A-C, T-G", "모두 동일"], 1),
    ("파동", "다음은 파동이다. 진폭은?", ["높이", "길이", "속도", "주기"], 1),
    ("전기 회로", "전류 방향은?", ["양→음", "음→양", "무작위", "없음"], 1),
    ("광합성", "필요하지 않은 것은?", ["빛", "물", "산소", "이산화탄소"], 3),
    ("지층", "가장 오래된 층은?", ["위", "중간", "아래", "모름"], 3),
    ("에너지", "운동 에너지는?", ["정지", "움직임", "열", "빛"], 2),
]


def get_chrome_service() -> Optional[Service]:
    driver_path = os.getenv("GAEUN_CHROMEDRIVER_PATH")
    if driver_path:
        return Service(executable_path=driver_path)
    return None


def create_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = get_chrome_service()
    try:
        if service:
            return webdriver.Chrome(service=service, options=options)
        return webdriver.Chrome(options=options)
    except WebDriverException as exc:
        raise RuntimeError(
            "Chrome WebDriver를 실행할 수 없습니다. GAEUN_CHROMEDRIVER_PATH 환경 변수를 확인하거나 드라이버를 설치하세요."
        ) from exc


def get_first_image_url(driver: webdriver.Chrome, query: str) -> Optional[str]:
    driver.get("https://www.google.com/imghp")
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(f"{query} 이미지 png")
        search_box.send_keys(Keys.RETURN)

        images = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.Q4LuWd"))
        )
        if not images:
            return None

        images[0].click()
        actual_images = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.n3VNCb"))
        )
        for img in actual_images:
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                return src
    except (NoSuchElementException, TimeoutException) as exc:
        logger.warning("이미지 검색 중 오류가 발생했습니다: %s", exc)
    return None


def generate_science_questions_json(output_path: str = "science_questions.json") -> int:
    driver = create_driver()
    result = []

    try:
        for idx, (keyword, question, choices, answer) in enumerate(DEFAULT_QUESTIONS, start=1):
            print(f"[{idx}] 검색중: {keyword}")
            image_url = get_first_image_url(driver, keyword)
            result.append(
                {
                    "id": idx,
                    "subject": "통합과학1",
                    "type": "객관식",
                    "question": question,
                    "image": image_url,
                    "choices": choices,
                    "answer": answer,
                }
            )

        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
        return len(result)
    finally:
        driver.quit()
