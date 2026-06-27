import webbrowser
import urllib.parse
import time

keywords = [
    "빗살무늬 토기",
    "고인돌",
    "비파형 동검",
    "광개토대왕릉비",
    "무령왕릉",
    "신라 금관",
    "불국사",
    "석굴암",
    "살수대첩",
    "안시성",
    "발해",
    "성덕대왕신종",
    "고려 청자",
    "팔만대장경",
    "직지심체요절",
    "고구려 벽화",
    "금동대향로",
    "천마총",
    "화랑도",
    "황산벌 전투",
    "빅뱅 우주론",
    "주기율표",
    "공유 결합",
    "이온 결합",
    "별의 진화",
    "원소의 탄생"
]

base_url = "https://namu.wiki/Search?q="

for k in keywords:
    encoded = urllib.parse.quote(k)
    url = base_url + encoded
    webbrowser.open(url)
    time.sleep(1)