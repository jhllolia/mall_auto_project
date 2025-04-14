import pandas as pd

def save_to_excel(parsed_rows, file_path="주문리스트_예시.xlsx"):
    columns = [
        "번호",
        "구매자명",
        "상품명",
        "옵션",
        "수량",
        "배송지",
        "연락처",
        "구매경로",
        "배송비",
        "과세",
        "면세",
        "배송 메세지"
    ]
    df = pd.DataFrame(parsed_rows, columns=columns)
    df.to_excel(file_path, index=False)
    print(f"✅ 엑셀 저장 완료: {file_path}")
