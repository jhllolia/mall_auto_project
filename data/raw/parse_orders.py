def parse_orders_for_spreadsheet(order_data):
    rows = []

    # 단건이면 리스트로 감싸기
    if isinstance(order_data, dict):
        order_data_list = [order_data]
    elif isinstance(order_data, list):
        order_data_list = order_data
    else:
        raise ValueError("올바르지 않은 JSON 구조입니다.")

    order_number = 1
    for order_item in order_data_list:
        contents = order_item.get("data", {}).get("contents", [])

        # orderId 기준으로 그룹핑
        grouped_orders = {}
        for item in contents:
            content = item.get("content", {})
            order = content.get("order", {})
            order_id = order.get("orderId")
            grouped_orders.setdefault(order_id, []).append(item)

        for order_id, group_items in grouped_orders.items():
            order_rows = []
            for item in group_items:
                content = item.get("content", {})
                order = content.get("order", {})
                product = content.get("productOrder", {})
                shipping = product.get("shippingAddress", {})

                buyer_name = order.get("ordererName", "")
                product_name = product.get("productName", "")
                option = product.get("productOption", "")
                quantity = product.get("quantity", 1)
                address = f"{shipping.get('baseAddress', '')} {shipping.get('detailedAddress', '')}".strip()
                phone = shipping.get("tel1", "")
                inflow_path = product.get("inflowPath", "네이버")
                delivery_fee = product.get("deliveryFeeAmount", 0)
                memo = product.get("shippingMemo", "")
                unit_price = product.get("unitPrice", 0)

                # 과세/면세 구분
                name_check = product_name + option
                if "순대" in name_check:
                    tax = unit_price
                    tax_free = ""
                elif "돼지머리" in name_check or "내장" in name_check:
                    tax = ""
                    tax_free = unit_price
                else:
                    tax = ""
                    tax_free = ""

                order_rows.append({
                    "번호": order_number,
                    "구매자명": buyer_name,
                    "상품명": product_name,
                    "옵션": option,
                    "수량": quantity,
                    "배송지": address,
                    "연락처": phone,
                    "구매경로": inflow_path,
                    "배송비": delivery_fee,
                    "과세": tax,
                    "면세": tax_free,
                    "배송 메세지": memo
                })

            # 정렬: 메인 > 순대류 > 내장류 > 기타
            def sort_key(item):
                name = item["상품명"] + item["옵션"]
                if any(kw in name for kw in ["돼지머리", "돈내장"]):
                    return 0
                elif "순대" in name:
                    return 1
                elif any(opt in name for opt in ["오소리감투", "소창", "간", "허파", "염통", "울대"]):
                    return 2
                elif "아이스팩" in name:
                    return 3
                else:
                    return 4

            order_rows.sort(key=sort_key)

            for i, item in enumerate(order_rows):
                if i == 0:
                    row = [
                        item["번호"], item["구매자명"], item["상품명"], item["옵션"], item["수량"],
                        item["배송지"], item["연락처"], item["구매경로"], item["배송비"],
                        item["과세"], item["면세"], item["배송 메세지"]
                    ]
                else:
                    row = [
                        item["번호"], "", item["상품명"], item["옵션"], item["수량"],
                        "", "", "", "", item["과세"], item["면세"], ""
                    ]

                rows.append(row)

            rows.append([""] * 12)
            order_number += 1

    return rows