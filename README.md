# mall_auto_project

main.py                             전체 작업을 스케줄링하거나 실행하는 진입점입니다.
config/settings.py                  환경변수나 경로, API 키 등을 정리해 관리합니다.
naver_smartstore/fetch_orders.py	주문 데이터를 수집하는 핵심 모듈입니다.
db/	                                SQLite 또는 MySQL 같은 DB를 연동할 경우 사용하는 모듈입니다.
sheets/upload_to_sheet.py	        구글 시트 API를 사용하여 데이터를 업로드합니다.
utils/helpers.py	                날짜 처리, 문자열 처리 등의 공통 기능을 담습니다.
test/	                            각 기능 테스트를 구현할 수 있습니다.