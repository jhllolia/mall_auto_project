import requests
import logging
from datetime import datetime
from config import settings

# 조회할 기간 설정
start_date = "2025-04-01"
end_date = "2025-04-31"

# ISO 포맷으로 변환
start_datetime = f"{start_date}T00:00:00"
end_datetime = f"{end_date}T23:59:59"

# 기본 URL
BASE_URL = "https://api.commerce.naver.com/external/v1"

# 요청 헤더
HEADERS = {
    "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    "Content-Type": "application/json",
}

# 주문 데이터 조회
def fetch_orders():
    page = 1
    page_size = 100
    all_orders = []

    while True:
        url = (
            f"{BASE_URL}/orders?"
            f"lastChangeFrom={start_datetime}&"
            f"lastChangeTo={end_datetime}&"
            f"page={page}&pageSize={page_size}"
        )

        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            logging.error(f"주문 조회 실패: {response.status_code} - {response.text}")
            break

        data = response.json()
        orders = data.get("data", {}).get("orderProducts", [])

        if not orders:
            break

        all_orders.extend(orders)
        print(f"{len(orders)}건 불러옴 (페이지 {page})")

        # 더 이상 다음 페이지가 없으면 중단
        if not data.get("data", {}).get("hasNext", False):
            break

        page += 1

    return all_orders

if __name__ == "__main__":
    orders = fetch_orders()
    print(f"총 {len(orders)}건의 주문 데이터를 가져왔습니다.\n")

    for order in orders:
        print(order)