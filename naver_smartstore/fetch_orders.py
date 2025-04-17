# naver_smartstore/fetch_orders.py

import requests
import logging, time, json
import bcrypt
import pybase64

from config import settings
from datetime import datetime
from zoneinfo import ZoneInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET

# 토큰생성
def generate_client_secret_sign(client_secret, timestamp):
    clientSecret = client_secret
    # 밑줄로 연결하여 password 생성
    password = client_id + "_" + str(timestamp)
    # bcrypt 해싱
    hashed = bcrypt.hashpw(password.encode('utf-8'), clientSecret.encode('utf-8'))
    # base64 인코딩
    return pybase64.standard_b64encode(hashed).decode('utf-8')

def get_access_token():
    timestamp = str(int(time.time() * 1000))  # UTC 밀리초
    client_secret_sign = generate_client_secret_sign(client_secret, timestamp)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    payload = {
        "client_id": client_id,
        "client_secret_sign": client_secret_sign,
        "grant_type": "client_credentials",
        "timestamp": timestamp,
        "type": "SELF"
    }

    response = requests.post(settings.TOKEN_URL, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(response.status_code, response.text)
        return None

def fetch_orders(start_date: str, end_date: str):
    token = get_access_token()

    if not token:
        return

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    start_obj = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo('Asia/Seoul'))
    end_obj = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo('Asia/Seoul'))

    from_dt = start_obj.isoformat(timespec='milliseconds')
    to_dt = end_obj.isoformat(timespec='milliseconds')

    order_params = {
        # "rangeType": "PAYED_DATETIME",
        # "productOrderStatuses": ["PAYED"],
        "from": from_dt,
        "to": to_dt,
        # "page": 1,
        # "pageSize": 1
    }

    response = requests.get(settings.ORDER_URL, headers=headers, params=order_params)

    if response.status_code == 200:
        return response.json()  # ✅ str 말고 json()으로 리턴
    else:
        logging.error(f"주문 요청 실패: {response.status_code} - {response.text}")
        return []

# if __name__ == "__main__":
#     fetch_orders()