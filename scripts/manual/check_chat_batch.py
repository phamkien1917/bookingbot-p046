import json
import time
import urllib.error
import urllib.request
import uuid

URL = "http://localhost:8000/api/v1/chat"
OUTPUT_FILE = "test_results.md"

# Kịch bản kiểm thử diện rộng
# Được chia thành nhiều chủ đề khác nhau để bao phủ 100+ câu hỏi
SCENARIOS = {
    # Nhóm 1: Cơ bản và khoảng cách (Khoảng cách tĩnh)
    "1.1. Lọc khoảng cách cơ bản": ["Tìm nhà ở Cầu Giấy dưới 3 tỷ.", "Lọc những căn cách Đại học Quốc gia dưới 2km."],
    "1.2. Khoảng cách thời gian": ["Nhà quận Ba Đình giá 5-7 tỷ.", "Chỉ lấy những căn đi xe đến Hồ Tây dưới 10 phút."],
    "1.3. Khoảng cách đi bộ": ["Chung cư mini quận Đống Đa.", "Tìm căn nào đi bộ ra ngã tư sở dưới 15 phút."],
    "1.4. Gộp tiêu chí ngay từ đầu": ["Tìm chung cư quận Hai Bà Trưng, giá dưới 4 tỷ, cách Bệnh viện Bạch Mai dưới 2km."],
    "1.5. Lọc khoảng cách cụ thể bằng mét": ["Nhà phố Cổ dưới 20 tỷ.", "Căn nào cách Hồ Gươm khoảng 500m không?"],

    # Nhóm 2: Tiện ích xung quanh (Nearby Places)
    "2.1. Tìm tiện ích Y Tế": ["Mua nhà Thanh Xuân, tài chính 4 tỷ.", "Xung quanh có bệnh viện hoặc trạm y tế nào không?"],
    "2.2. Tìm tiện ích Giáo dục": ["Tìm nhà đất quận Hà Đông 5 tỷ.", "Gần đó có trường mầm non hoặc trường cấp 1 nào không?"],
    "2.3. Tìm tiện ích Sinh hoạt": ["Chung cư Nam Từ Liêm.", "Gần căn này có siêu thị hay công viên nào cho trẻ em không?"],
    "2.4. Kết hợp khoảng cách và tiện ích": ["Tìm chung cư gần Bệnh viện E dưới 3km, yêu cầu xung quanh phải có trường học."],
    "2.5. Tiện ích đa dạng": ["Nhà mặt phố Cầu Giấy.", "Kiểm tra xem quanh đó có chợ, siêu thị và công viên không?"],

    # Nhóm 3: Giao tiếp đa lượt, thay đổi ý định (Multi-turn refinement)
    "3.1. Đổi ý khoảng cách": [
        "Tìm nhà cách Bến xe Mỹ Đình dưới 1km.",
        "Hình như hơi ít kết quả, nới rộng ra 3km xem sao.",
        "Thôi, tìm cho tôi cách bến xe Nước Ngầm 2km đi."
    ],
    "3.2. Thay đổi tiện ích": [
        "Có nhà nào ở Long Biên giá dưới 6 tỷ không?",
        "Gần đó có trường học không?",
        "À quên, xem thử gần đó có bệnh viện nào lớn không?"
    ],
    "3.3. Đổi vùng tìm kiếm": [
        "Nhà ở Hoàng Mai dưới 3 tỷ.",
        "Cách bến xe Giáp Bát bao xa?",
        "Thôi đổi sang quận Thanh Xuân đi, cách Ngã tư sở 2km."
    ],

    # Nhóm 4: Các trường hợp nhiễu, lỗi chính tả, phương ngữ (Robustness)
    "4.1. Sai lỗi chính tả (Typos)": ["Tym nhà ở đống đâ tài trính 5 tỏi.", "Cách đh Bác Khao dươi 2 cây số."],
    "4.2. Viết tắt (Slang)": ["Tìm cc ở HN, giá dứi 3 củ to.", "Cách bv ĐH Y bn km?"],
    "4.3. Không có chủ ngữ": ["Cầu Giấy, 4 tỷ, 2 phòng ngủ.", "Cách ĐHQG 2km."],
    "4.4. Đơn vị lạ": ["Nhà ở Ba Đình.", "Cách lăng Bác dưới hai ngàn mét."],

    # Nhóm 5: Các vị trí ảo hoặc nằm ngoài dữ liệu (Out of scope/Fallback)
    "5.1. Vị trí nước ngoài": ["Tìm nhà ở Hà Nội.", "Khoảng cách từ nhà đó đến tháp Tokyo là bao nhiêu?"],
    "5.2. Vị trí ở tỉnh khác": ["Tìm nhà chung cư Hà Nội.", "Cách chợ Bến Thành bao xa?"],
    "5.3. Tiện ích không tồn tại": ["Tìm nhà gần Rừng rậm Amazon."],
    "5.4. Không xác định được toạ độ": ["Tìm nhà cách nhà chú vượng dưới 2km."],

    # Nhóm 6: Hỏi trực tiếp về khoảng cách một nhà cụ thể (Giả định Bot đã gợi ý nhà)
    "6.1. Chi tiết một nhà": ["Tìm nhà ở Đống Đa.", "Căn rẻ nhất cách bệnh viện Xanh Pôn bao nhiêu phút?"],
    "6.2. So sánh khoảng cách": ["Nhà Cầu Giấy.", "Căn nào gần ngã tư Cầu Giấy hơn?"],
    "6.3. Tiện ích chi tiết": ["Căn ở Nam Từ Liêm.", "Bán kính 1km quanh căn này có gì chơi không?"]
}

# Sinh thêm các phiên bản tự động để đủ 100 câu hỏi
for i in range(1, 15):
    SCENARIOS[f"7.{i}. Batch sinh tự động (Đường chim bay vs Thực tế)"] = [
        f"Tìm nhà ở quận {['Hoàn Kiếm', 'Đống Đa', 'Tây Hồ', 'Cầu Giấy', 'Hà Đông'][i%5]}.",
        f"Cách {'Hồ Tây' if i%2==0 else 'Bệnh viện 108'} khoảng {i} km.",
        "Quanh đó có siêu thị không?"
    ]

for i in range(1, 15):
    SCENARIOS[f"8.{i}. Batch so sánh ngân sách và vị trí"] = [
        f"Tìm nhà giá {i} tỷ ở Hà Nội.",
        f"Phải gần bến xe {'Mỹ Đình' if i%3==0 else 'Giáp Bát'} dưới {i*5} phút đi bộ."
    ]

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
    total_questions = sum(len(msgs) for msgs in SCENARIOS.values())
    print(f"BẮT ĐẦU CHẠY KIỂM THỬ: {len(SCENARIOS)} Kịch bản, {total_questions} Câu hỏi.")
    print(f"KẾT QUẢ SẼ ĐƯỢC LƯU VÀO FILE: {OUTPUT_FILE}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# BÁO CÁO KẾT QUẢ TEST GOONG API & CHAT\n")
        f.write(f"Tổng số kịch bản: {len(SCENARIOS)}\n")
        f.write(f"Tổng số câu hỏi: {total_questions}\n\n")

        for scenario_name, messages in SCENARIOS.items():
            print(f"\n▶ Đang xử lý: {scenario_name} ({len(messages)} turns)...")
            f.write(f"## {scenario_name}\n")
            session_id = str(uuid.uuid4())

            for idx, msg in enumerate(messages):
                print(f"  - Lượt {idx+1}: {msg[:30]}...")
                f.write(f"**👤 Lượt {idx+1} (User):** {msg}\n")

                start_time = time.time()
                result = send_message(msg, session_id)
                elapsed = time.time() - start_time

                if "error" in result:
                    f.write(f"> ❌ **LỖI:** {result['error']}\n\n")
                    continue

                f.write(f"> 🤖 **Agent ({elapsed:.1f}s):** {result.get('response')}\n\n")

                # In ra Insights
                insights = result.get("insights", {})
                if insights:
                    f.write(f"  - *Insights:* `{json.dumps(insights, ensure_ascii=False)}`\n")

                # In ra Properties
                properties = result.get("properties", [])
                if properties:
                    f.write(f"  - *Số nhà tìm thấy:* {len(properties)}\n")
                    for p in properties:
                        ev_dist = p.get("distance_evidence")
                        ev_near = p.get("nearby_evidence")
                        if ev_dist:
                            f.write(f"    - Nhà {p.get('id')}: {ev_dist.get('distance_km')}km, {ev_dist.get('duration_minutes')}phút (tới {ev_dist.get('destination')})\n")
                        if ev_near:
                            f.write(f"    - Nhà {p.get('id')}: Có tiện ích xung quanh.\n")
                f.write("\n")
                time.sleep(1) # Nghỉ 1 chút tránh quá tải API

    print(f"\nĐÃ HOÀN THÀNH TOÀN BỘ. Vui lòng kiểm tra file {OUTPUT_FILE} để xem chi tiết.")

if __name__ == "__main__":
    run_tests()
