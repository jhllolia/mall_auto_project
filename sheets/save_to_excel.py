import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Side, PatternFill

def save_to_excel(rows, file_path="주문리스트_예시.xlsx"):
    columns = [
        "번호", "구매자명", "상품명", "옵션", "수량",
        "배송지", "연락처", "구매경로", "배송비", "과세", "면세", "배송 메세지"
    ]

    df = pd.DataFrame(rows, columns=columns)
    df.to_excel(file_path, index=False)

    wb = load_workbook(file_path)
    ws = wb.active

    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )
    gray_fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        is_separator = all(cell.value in ("", None) for cell in row)
        for cell in row:
            cell.alignment = center
            cell.border = thin_border
            if is_separator:
                cell.fill = gray_fill

    wb.save(file_path)
    print(f"✅ 엑셀 저장 완료: {file_path}")
