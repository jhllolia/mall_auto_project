# 메인 실행 파일 (자동화 스케줄링 포함)
import logging
import json

from datetime import datetime

from naver_smartstore.fetch_orders import fetch_orders
from data.raw.parse_orders import parse_orders_for_spreadsheet
from sheets.save_to_excel import save_to_excel  # 같은 디렉토리에 저장했다면

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# ✅ True면 로컬 JSON 파일에서 읽음, False면 API 호출
USE_LOCAL_JSON = False

def load_orders_from_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"로컬 파일에서 주문 데이터를 불러왔습니다: {filepath}")
            return data
    except FileNotFoundError:
        logger.error(f"파일을 찾을 수 없습니다: {filepath}")
        return []

if __name__ == "__main__":

    if USE_LOCAL_JSON:
        with open("data/sample_order.json", "r", encoding="utf-8") as f:
            orders = json.load(f)
    else:
        start_date = "2025-04-14 00:00:00"
        end_date = "2025-04-15 00:00:00"

        orders = fetch_orders(start_date, end_date)

    # print("orders :",orders)
    parsed_rows = parse_orders_for_spreadsheet(orders)
    # print("parsed_rows :",parsed_rows)
    save_to_excel(parsed_rows, "주문리스트_예시.xlsx")

    # for row in parsed_rows:
    #     print("\t".join(map(str, row)))

    # ▶ 여기서 원하는 출력/처리 작업을 하면 됩니다.
    # for order in orders:
    #     contents = order.get("data", {}).get("contents", [])

    #     for item in contents:
    #         content = order.get('content', {})
    #         order_info = content.get('order', {})
    #         product_order = content.get('productOrder', {})
    #         shipping_address = product_order.get('shippingAddress', {})

