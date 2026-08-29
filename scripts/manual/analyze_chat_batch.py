import re


def analyze_results():
    with open("eval/results/goong_chat_batch_2026-08-28.md", encoding="utf-8") as f:
        content = f.read()

    # Count total turns
    turns = re.findall(r"\*\*👤 Lượt \d+ \(User\):\*\*", content)
    total_turns = len(turns)

    # Count errors
    errors = re.findall(r"> ❌ \*\*LỖI:\*\*", content)
    total_errors = len(errors)

    # Count distance and nearby evidence triggers
    distances = len(re.findall(r"km, \d+(?:\.\d+)?phút", content))
    nearbys = len(re.findall(r"Có tiện ích xung quanh", content))

    # Check for "Đã xác minh bằng Goong" text
    goong_verified = len(re.findall(r"Đã xác minh bằng Goong", content))

    # Check for Fallback scenarios (Group 5)
    fallback_section = content.split("## 5.1.")[-1].split("## 6.1.")[0] if "## 5.1." in content else ""

    print("=== KẾT QUẢ PHÂN TÍCH ====================")
    print(f"Tổng số lượt hỏi: {total_turns}")
    print(f"Số lượt bị lỗi HTTP/Code: {total_errors}")
    print(f"Số lượng nhà được lọc khoảng cách thành công: {distances}")
    print(f"Số lượng nhà tìm thấy tiện ích xung quanh: {nearbys}")
    print(f"Số câu trả lời nhắc đến Goong: {goong_verified}")
    print("\n--- Fallback Analysis ---")
    if "Tokyo" in fallback_section or "Eiffel" in fallback_section or "Amazon" in fallback_section:
        print("Hệ thống đã nhận diện được các địa điểm ảo/nước ngoài.")
    else:
        print("Không tìm thấy dữ liệu nhóm 5.")

    print("=========================================")

if __name__ == "__main__":
    analyze_results()
