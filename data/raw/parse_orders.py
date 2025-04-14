def parse_orders_for_spreadsheet(order_data):
    rows = []
    contents = order_data.get("data", {}).get("contents", [])

    for idx, item in enumerate(contents, start=1):
        content = item.get("content", {})
        order = content.get("order", {})
        product_order = content.get("productOrder", {})
        shipping_address = product_order.get("shippingAddress", {})

        # 기본 필드 추출
        buyer_name = order.get("ordererName", "")
        product_name = product_order.get("productName", "")
        product_option = product_order.get("productOption", "")
        quantity = product_order.get("quantity", 1)
        address = f"{shipping_address.get('baseAddress', '')} {shipping_address.get('detailedAddress', '')}".strip()
        phone = shipping_address.get("tel1", "")
        route = "네이버"
        shipping_fee = product_order.get("deliveryFeeAmount", 0)
        message = product_order.get("shippingMemo", "")

        # 과세 / 면세 금액 판별 (기본은 과세로 가정)
        unit_price = product_order.get("unitPrice", 0)
        if "내장" in product_name or "돼지머리" in product_name:
            tax = 0
            tax_free = unit_price
        else:
            tax = unit_price
            tax_free = 0

        row = [
            idx,
            buyer_name,
            product_name,
            product_option,
            quantity,
            address,
            phone,
            route,
            shipping_fee,
            tax,
            tax_free,
            message
        ]
        rows.append(row)

    return rows
