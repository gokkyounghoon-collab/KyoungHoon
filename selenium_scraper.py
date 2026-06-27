import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------
# 구글 이미지 1번 URL 가져오기
# -------------------------------
def get_first_image_url(driver, query):
    driver.get("https://www.bing.com/images/search?q=" + query + " 이미지")

    time.sleep(5)  # 검색 결과 대기

    # Bing 이미지 selector
    images = driver.find_elements(By.CSS_SELECTOR, ".iusc img")

    if not images:
        return None

    # 첫 번째 이미지의 src 가져오기
    src = images[0].get_attribute("src")
    if src and src.startswith("http") and not src.startswith("data:"):
        return src

    # data-src 시도
    data_src = images[0].get_attribute("data-src")
    if data_src and data_src.startswith("http"):
        return data_src

    return None


# -------------------------------
# 문제 데이터 (기본 템플릿)
# -------------------------------
questions = [
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

# -------------------------------
# 드라이버 실행
# -------------------------------
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # headless 제거
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-minimized")  # 창 최소화
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=options)

result = []

# -------------------------------
# 문제 생성
# -------------------------------
for idx, (keyword, question, choices, answer) in enumerate(questions, start=1):
    print(f"[{idx}] 검색중: {keyword}")

    image_url = get_first_image_url(driver, keyword)

    result.append({
        "id": idx,
        "subject": "통합과학1",
        "type": "객관식",
        "question": question,
        "image": image_url,
        "choices": choices,
        "answer": answer
    })

driver.quit()

# -------------------------------
# JSON 저장
# -------------------------------
with open("science_questions.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("완료: science_questions.json 생성됨")