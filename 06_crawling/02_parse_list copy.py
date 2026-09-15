import requests, json, csv
from bs4 import BeautifulSoup
from config import BASE, TIMEOUT, HEADERS
from parsers import parse_stocks

resp = requests.get(
    f"{BASE}/stocks",
    params={"sector": "S08", "market": "", "q": ""},
    headers=HEADERS,
    timeout=TIMEOUT
)
resp.raise_for_status() 

html = resp.text
soup = BeautifulSoup(html, 'lxml')

stocks = parse_stocks(html)

print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>12}{'등락률':>9}")
for s in stocks:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")
print("="*60)

# json 저장하기
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# csv 저장하기
def save_csv(data, path):
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        # fieldnames -> 컬럼 순서
        writer.writeheader()        # csv 파일 맨 첫줄에 컬럼 이름들로 씀
        writer.writerows(data)
              # 딕셔너리 리스트 전체를 각각의 행으로 씀(기록)

save_json(stocks, "stocks_it서비스.json")
save_csv(stocks, "stocks_it서비스.csv")