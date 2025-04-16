import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Side


def save_to_excel(rows, file_path="주문리스트_예시.xlsx"):
    columns = [
        "번호", "구매자명", "상품명", "옵션", "수량",
        "배송지", "연락처", "구매경로", "배송비", "과세", "면세", "배송 메세지"
    ]

    # separator 줄 제거 없이 DataFrame 생성
    df = pd.DataFrame([row if any(cell != "" for cell in row) else [None]*len(columns) for row in rows], columns=columns)
    df.to_excel(file_path, index=False)

    wb = load_workbook(file_path)
    ws = wb.active

    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )
    thick_black_border = Border(
        top=Side(style="thick", color="000000"),
        left=Side(style="thin"), right=Side(style="thin"), bottom=Side(style="thin")
    )

    previous_order_number = None
    for i, row in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row), start=2):
        is_separator = all(cell.value in ("", None) for cell in row)
        print("is_separator :",is_separator)
        current_order_number = row[0].value

        for j, cell in enumerate(row):
            col_letter = ws.cell(row=1, column=j+1).value

            # 구매경로 표기 간소화
            if col_letter == "구매경로" and cell.value:
                cell.value = "쿠팡" if "쿠팡" in str(cell.value) else "네이버"

            # 번호는 같은 주문에 대해서는 한 번만 출력
            if col_letter == "번호":
                if current_order_number == previous_order_number:
                    cell.value = ""
                else:
                    previous_order_number = current_order_number

            # 좌측 정렬 열
            if j in [1, 5, 6, 11] and ws.cell(row=i, column=2).value != "":
                cell.alignment = left
            else:
                cell.alignment = center

            # 구분선 처리
            if is_separator:
                cell.border = thick_black_border
            else:
                cell.border = thin_border

    # 열 너비 고정 설정
    col_widths = [6, 12, 28, 22, 6, 35, 15, 10, 10, 10, 10, 25]
    for i, width in enumerate(col_widths, start=1):
        col_letter = chr(64 + i) if i <= 26 else chr(64 + (i - 1) // 26) + chr(64 + (i - 1) % 26 + 1)
        ws.column_dimensions[col_letter].width = width

    wb.save(file_path)
    print(f"✅ 엑셀 저장 완료: {file_path}")