import urllib.request
import urllib.error
import json
import sys

def test_chat():
    url = "http://localhost:8000/api/v1/chat"
    payload = {
        "message": "Tìm nhà gần Bệnh viện Đa khoa dưới 5km",
        "session_id": "12345678-1234-5678-1234-567812345678"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    
    print("Đang gửi yêu cầu đến Agent...")
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            print("\n--- THÀNH CÔNG ---")
            print("Phản hồi từ Agent:", result.get("response"))
            print("\nInsights (Phân tích của hệ thống):", json.dumps(result.get("insights", {}), ensure_ascii=False, indent=2))
            
            # Print distance evidence from properties if any
            properties = result.get("properties", [])
            print(f"\nSố lượng nhà tìm thấy: {len(properties)}")
            for p in properties:
                evidence = p.get("distance_evidence")
                if evidence:
                    print(f" - Nhà ID {p.get('id')}: Cách {evidence.get('distance_km')} km (Bởi {evidence.get('provider')})")
                else:
                    print(f" - Nhà ID {p.get('id')}: Không có thông tin khoảng cách")
                    
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"\nLỖI HTTP {e.code}: {body}")
        return False
    except Exception as e:
        print(f"\nLỖI KHÔNG XÁC ĐỊNH: {e}")
        return False

if __name__ == "__main__":
    success = test_chat()
    if not success:
        sys.exit(1)
