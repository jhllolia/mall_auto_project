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

        for content_item in contents:
            content = content_item.get("content", {})
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
            if "순대" in product_name:
                tax = unit_price
                tax_free = ""
            elif "돼지머리" in product_name or "내장" in product_name:
                tax = ""
                tax_free = unit_price
            else:
                tax = ""
                tax_free = ""

            row = [
                order_number,
                buyer_name,
                product_name,
                option,
                quantity,
                address,
                phone,
                inflow_path,
                delivery_fee,
                tax,
                tax_free,
                memo
            ]
            rows.append(row)

        # 회색 구분 줄
        rows.append([""] * 12)
        order_number += 1

    return rows