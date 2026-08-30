import json
import time
import urllib.request
import uuid


def test_api():
    base_url = 'https://bookingbot-api-q0t9.onrender.com'
    print("=" * 65)
    print("🔍 KIỂM THỬ THỰC ĐỊA PRODUCTION CLOUD (RENDER LIVE)")
    print(f"⏰ Thời điểm kiểm thử: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    # 1. Warmup / Health check with retry
    print("1. Đang gửi tín hiệu đánh thức (Warm-up) Render...")
    health_ok = False
    for attempt in range(1, 4):
        t0 = time.time()
        try:
            with urllib.request.urlopen(f"{base_url}/health", timeout=60) as res:
                lat = time.time() - t0
                data = json.loads(res.read().decode())
                print(f"   [Lần {attempt}] Health Check: HTTP {res.status} ({lat:.2f}s) -> Payload: {data}")
                health_ok = True
                break
        except Exception as e:
            lat = time.time() - t0
            print(f"   [Lần {attempt}] Đang chờ Render khởi động ({lat:.2f}s)... Lỗi: {e}")
            time.sleep(5)

    if not health_ok:
        print("❌ Không thể kết nối tới Render.")
        return

    # 2. Chat Turn 1: Search Property
    session_id = str(uuid.uuid4())
    url = f"{base_url}/api/v1/chat"
    payload = {
        "message": "Tìm căn hộ 2 phòng ngủ ở quận Cầu Giấy dưới 5 tỷ",
        "session_id": session_id
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})

    print("\n2. Chat Lượt 1 (Tìm kiếm BĐS Cầu Giấy < 5 tỷ):")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            lat = time.time() - t0
            data = json.loads(res.read().decode("utf-8"))
            print(f"   -> HTTP {res.status} | Độ trễ thực tế: {lat:.2f}s")
            print(f"   -> ai_mode: {data.get('ai_mode')}")
            print(f"   -> ai_model: {data.get('ai_model')}")
            print(f"   -> Số BĐS tìm thấy: {len(data.get('properties', []))}")
            print(f"   -> Response trích đoạn: {data.get('response', '')[:130]}...")
    except Exception as e:
        print(f"   -> Chat Turn 1 Failed: {e}")

    # 3. Chat Turn 2: Warm Call
    payload2 = {
        "message": "Có căn nào diện tích trên 50m2 không bạn?",
        "session_id": session_id
    }
    req2 = urllib.request.Request(url, data=json.dumps(payload2).encode(), headers={"Content-Type": "application/json"})
    print("\n3. Chat Lượt 2 (Máy đã nóng - Kế thừa Cầu Giấy, lọc > 50m2):")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req2, timeout=60) as res:
            lat = time.time() - t0
            data = json.loads(res.read().decode("utf-8"))
            print(f"   -> HTTP {res.status} | Độ trễ thực tế: {lat:.2f}s")
            print(f"   -> ai_mode: {data.get('ai_mode')}")
            print(f"   -> Số BĐS tìm thấy: {len(data.get('properties', []))}")
            print(f"   -> Response trích đoạn: {data.get('response', '')[:130]}...")
    except Exception as e:
        print(f"   -> Chat Turn 2 Failed: {e}")

    # 4. Chat Turn 3: Booking Request
    payload3 = {
        "message": "Tôi muốn đặt lịch xem căn số 1 vào sáng mai lúc 9 giờ.",
        "session_id": session_id
    }
    req3 = urllib.request.Request(url, data=json.dumps(payload3).encode(), headers={"Content-Type": "application/json"})
    print("\n4. Chat Lượt 3 (Yêu cầu đặt lịch xem nhà sáng mai 9h):")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req3, timeout=60) as res:
            lat = time.time() - t0
            data = json.loads(res.read().decode("utf-8"))
            print(f"   -> HTTP {res.status} | Độ trễ thực tế: {lat:.2f}s")
            print(f"   -> ai_mode: {data.get('ai_mode')}")
            print(f"   -> Response trích đoạn: {data.get('response', '')[:130]}...")
    except Exception as e:
        print(f"   -> Chat Turn 3 Failed: {e}")

    print("\n" + "=" * 65)
    print("✅ HOÀN TẤT ĐO ĐẠC THỰC ĐỊA TRÊN CLOUD!")
    print("=" * 65)

if __name__ == "__main__":
    test_api()
