"""Knowledge Base service cho FAQ và thông tin BĐS.

Dùng để trả lời nhanh các câu hỏi phổ biến mà không cần gọi LLM.
Hỗ trợ cả FAQ tĩnh và search động từ database.
"""

import logging

from src.database.models import Property

logger = logging.getLogger(__name__)


# ============== Static FAQ ==============
# Câu hỏi phổ biến và câu trả lời nhanh
# Key là lowercase để search

FAQ_KNOWLEDGE = {
    # Chung
    "chào|xin chao|hello|hi": {
        "response": "Xin chào! 👋 Tôi là BookingBot, trợ lý AI của công ty bất động sản. Tôi có thể giúp bạn tìm kiếm bất động sản và đặt lịch xem nhà. Bạn cần hỗ trợ gì hôm nay?",
        "category": "greeting"
    },

    # CCMN 13 - Thông tin dự án
    "ccmn|ccmn 13|chung cư misora|chung cu misora":
        {
            "response": """**Chung Cư Misora 13 (CCMN13) - Phường Trung Mỹ Tây, Quận 12**

📍 **Địa chỉ:** 13 Đường Trung Mỹ Tây 13, Phường Trung Mỹ Tây, Quận 12, TP.HCM

🏢 **Thông tin dự án:**
- **Loại:** Căn hộ chung cư
- **Số tầng:** 13 tầng
- **Số phòng:** Khép kín
- **Quận:** Quận 12
- **Phường:** Trung Mỹ Tây

💰 **Giá tham khảo:** Liên hệ để biết giá chi tiết

📞 Để được tư vấn về CCMN13, vui lòng liên hệ hoặc tôi sẽ cập nhật thông tin cho bạn.

Bạn có muốn tôi tìm các căn hộ khác ở Quận 12 không?""",
            "category": "project_info"
        },

    # Doanh thu
    "doanh thu|revenue|lợi nhuận|profit":
        {
            "response": """**Về thông tin doanh thu bất động sản:**

Tôi không có thông tin doanh thu cụ thể của các dự án. Để biết thêm chi tiết, bạn nên:

1. Liên hệ trực tiếp chủ đầu tư
2. Tham khảo báo cáo tài chính của công ty
3. Hỏi nhân viên tư vấn tại sàn giao dịch

Tôi có thể giúp bạn tìm thông tin về:
- Bất động sản cho thuê với thu nhập ổn định
- Các dự án có tiềm năng cho thuê tốt
- So sánh giá và lợi nhuận giữa các khu vực

Bạn muốn tìm hiểu thêm về chủ đề nào?""",
            "category": "finance"
        },

    # Giờ làm việc
    "giờ làm|thời gian mở|cửa|mấy giờ":
        {
            "response": "🏢 **Giờ làm việc:**\n- Thứ 2 - Thứ 6: 8:00 - 18:00\n- Thứ 7: 8:00 - 12:00\n- Chủ nhật: Nghỉ\n\nBạn có muốn đặt lịch xem nhà không?",
            "category": "general"
        },

    # Liên hệ
    "liên hệ|contact|phone|sdt|điện thoại":
        {
            "response": "📞 **Liên hệ tư vấn:**\n- Hotline: 0901 234 567\n- Email: contact@company.com\n\nBạn cần hỗ trợ gì thêm?",
            "category": "contact"
        },

    # Mua nhà lần đầu
    "lần đầu|mua nhà lần đầu|first time":
        {
            "response": """🏠 **Hướng dẫn mua nhà lần đầu:**

1. **Xác định ngân sách** - Tính toán khả năng tài chính
2. **Chọn khu vực** - Ưu tiên gần nơi làm việc, tiện đi lại
3. **Kiểm tra pháp lý** - Đảm bảo sổ đỏ, giấy tờ rõ ràng
4. **Kiểm tra thực tế** - Xem nhà, đánh giá chất lượng xây dựng
5. **Thương lượng** - So sánh giá, đàm phán tốt nhất
6. **Ký hợp đồng** - Đọc kỹ điều khoản

Tôi có thể giúp bạn tìm căn hộ phù hợp với ngân sách của bạn. Bạn muốn tìm ở khu vực nào?""",
            "category": "guide"
        },
}


def search_knowledge(query: str) -> dict | None:
    """Search trong knowledge base.

    Args:
        query: Câu hỏi của user

    Returns:
        Dict với response và category, hoặc None nếu không tìm thấy
    """
    query_lower = query.lower().strip()

    for keywords, data in FAQ_KNOWLEDGE.items():
        keyword_list = [k.strip() for k in keywords.split("|")]
        for keyword in keyword_list:
            if keyword in query_lower:
                return {
                    "found": True,
                    "response": data["response"],
                    "category": data["category"],
                    "confidence": 0.9,
                }

    return None


# ============== Dynamic Property Search ==============

async def search_property_by_name(name_query: str) -> dict | None:
    """Tìm kiếm bất động sản theo tên dự án.

    Args:
        name_query: Tên dự án cần tìm

    Returns:
        Thông tin dự án hoặc None
    """
    from sqlalchemy import or_, select

    from src.database.connection import get_session_context

    try:
        async with get_session_context() as session:
            # Tìm properties có title chứa từ khóa
            stmt = select(Property).where(
                or_(
                    Property.title.ilike(f"%{name_query}%"),
                    Property.district.ilike(f"%{name_query}%"),
                    Property.province.ilike(f"%{name_query}%"),
                )
            ).limit(5)

            result = await session.execute(stmt)
            properties = result.scalars().all()

            if properties:
                prop = properties[0]
                return {
                    "found": True,
                    "type": "property",
                    "data": {
                        "title": prop.title,
                        "price": prop.list_price,
                        "area": prop.area_sqm,
                        "bedrooms": prop.bedrooms,
                        "address": f"{prop.ward}, {prop.district}, {prop.province}",
                        "count": len(properties),
                    }
                }
    except Exception as e:
        logger.warning(f"Error searching property by name: {e}")

    return None


async def get_answer(query: str) -> str | None:
    """Lấy câu trả lời cho câu hỏi.

    Thứ tự ưu tiên:
    1. FAQ tĩnh (nhanh nhất)
    2. Search database BĐS
    3. Trả về None để dùng LLM

    Args:
        query: Câu hỏi của user

    Returns:
        Câu trả lời hoặc None
    """
    # 1. Thử FAQ tĩnh trước
    faq_result = search_knowledge(query)
    if faq_result and faq_result["confidence"] >= 0.8:
        return faq_result["response"]

    # 2. Thử search database
    import re
    # Trích xuất phần text trong ngoặc kép (nếu có) để tìm kiếm chính xác tên
    match = re.search(r'["\'](.*?)["\']', query)
    search_term = match.group(1) if match else query

    db_result = await search_property_by_name(search_term)
    if db_result and db_result["found"]:
        data = db_result["data"]
        response = f"""**{data['title']}**

📍 Địa chỉ: {data['address']}
📐 Diện tích: {data['area']} m²
🛏️ Phòng ngủ: {data['bedrooms']}
💰 Giá: {data['price']:,.0f} VND

"""
        if data['count'] > 1:
            response += f"Có {data['count']} căn phù hợp. Bạn muốn xem thêm không?"
        return response

    # 3. Không tìm thấy - trả về None để dùng LLM
    return None
