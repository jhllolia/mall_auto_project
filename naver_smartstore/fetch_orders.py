# naver_smartstore/fetch_orders.py

import requests
import logging, time, json
import bcrypt
import pybase64

from config import settings
from datetime import datetime, timedelta

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

def fetch_orders():
    token = get_access_token()

    if not token:
        return

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    order_params = {
        "rangeType": "PAYED_DATETIME",
        "productOrderStatuses": ["PAYED"],
        "from": "2025-04-12T12:00:00.000+09:00",
        "to": "2025-04-13T12:00:00.000+09:00",
    }

    response = requests.get(settings.ORDER_URL, headers=headers, params=order_params)
    print(response.status_code)
    # print(response.json())

if __name__ == "__main__":
    fetch_orders()