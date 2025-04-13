# 메인 실행 파일 (자동화 스케줄링 포함)

# main.py
from naver_smartstore.fetch_orders import fetch_orders

if __name__ == "__main__":
    # 조회 기간 설정
    fetch_orders()