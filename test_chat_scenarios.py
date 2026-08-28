import urllib.request
import urllib.error
import json
import uuid
import time
import sys

URL = "http://localhost:8000/api/v1/chat"

# Danh sách các kịch bản test (Scenarios)
# Mỗi kịch bản là một mảng các câu hỏi (mô phỏng 1 phiên chat nhiều lượt)
SCENARIOS = {
    "1. Lọc khoảng cách đa lượt (Routing)": [
        "Tôi muốn tìm một căn chung cư ở quận Hai Bà Trưng, có 2 phòng ngủ.",
        "Bạn lọc giúp tôi những căn nào cách Bệnh viện Bạch Mai dưới 3km được không?"
    ],
    "2. Tìm kiếm tiện ích xung quanh (Nearby Places)": [
        "Tìm giúp tôi nhà mặt phố ở Cầu Giấy, giá dưới 10 tỷ.",
        "Gần những căn bạn vừa tìm có trường học hoặc công viên nào không?"
    ],
    "3. Câu hỏi phức tạp gộp nhiều tiêu chí": [
        "Mình cần mua nhà đất ở Đống Đa, tài chính tầm 5-7 tỷ, yêu cầu cách ngã tư sở tối đa 10 phút đi xe."
    ],
    "4. Câu hỏi nằm ngoài vùng dữ liệu (Fallback)": [
        "Tìm cho tôi một căn nhà gỗ cách tháp Eiffel dưới 5km."
    ]
}

def send_message(message: str, session_id: str):
    payload = {
        "message": message,
        "session_id": session_id
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode('utf-8')}"}
    except Exception as e:
        return {"error": str(e)}

def run_tests():
    print("="*60)
    print("🚀 BẮT ĐẦU CHẠY KỊCH BẢN KIỂM THỬ BẢN ĐỒ (GOONG API)")
    print("="*60)
    
    for scenario_name, messages in SCENARIOS.items():
        print(f"\n\n▶ KỊCH BẢN: {scenario_name}")
        session_id = str(uuid.uuid4()) # Tạo Session ID mới cho mỗi kịch bản
        
        for idx, msg in enumerate(messages):
            print(f"\n👤 USER (Lượt {idx+1}): {msg}")
            print("⏳ Đang đợi Agent phản hồi...")
            
            start_time = time.time()
            result = send_message(msg, session_id)
            elapsed = time.time() - start_time
            
            if "error" in result:
                print(f"❌ LỖI: {result['error']}")
                break
                
            print(f"🤖 AGENT ({elapsed:.1f}s): {result.get('response')}")
            
            # In ra các insights thu thập được (nếu có)
            insights = result.get("insights", {})
            if insights:
                print("   [!] Insights thu được:", json.dumps(insights, ensure_ascii=False))
                
            # Kiểm tra bằng chứng khoảng cách (Distance Evidence)
            properties = result.get("properties", [])
            has_distance = any(p.get("distance_evidence") for p in properties)
            has_nearby = any(p.get("nearby_evidence") for p in properties)
            
            if has_distance:
                print(f"   [+] Đã kích hoạt tính năng khoảng cách (Goong Distance Matrix). Có {len(properties)} kết quả.")
            if has_nearby:
                print(f"   [+] Đã kích hoạt tính năng tìm tiện ích (Goong Places).")
                
            time.sleep(1) # Nghỉ 1 giây trước câu hỏi tiếp theo

if __name__ == "__main__":
    run_tests()
