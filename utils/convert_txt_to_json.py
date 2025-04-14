import json

# 텍스트(.txt) 파일 경로
txt_path = "data/simple_order.txt"
# 저장할 JSON 파일 경로
json_path = "data/sample_order.json"

with open(txt_path, "r", encoding="utf-8") as txt_file:
    content = txt_file.read()
    try:
        # 문자열을 JSON 객체로 파싱
        data = json.loads(content)

        # 리스트가 아닐 경우 리스트로 감싸기 (여러 건 처리 대비)
        if not isinstance(data, list):
            data = [data]

        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
            print(f"✅ 변환 성공: {json_path}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 변환 실패: {e}")
