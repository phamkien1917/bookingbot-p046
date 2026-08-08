import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database import async_session_maker
from datetime import datetime, timezone

async def seed():
    async with async_session_maker() as session:
        # Dữ liệu mẫu
        properties_data = [
            {
                "id": uuid.uuid4(),
                "code": "A-1208",
                "property_kind": "APARTMENT",
                "title": "Căn hộ A-1208, 2 phòng ngủ",
                "description": "Căn hộ cao cấp A-1208 với thiết kế tối giản và hiện đại. Không gian sống thoáng đãng, đón ánh sáng tự nhiên. Trang bị đầy đủ nội thất cao cấp nhập khẩu, hệ thống smarthome tiện nghi. Phù hợp cho gia đình trẻ hoặc chuyên gia nước ngoài.",
                "status": "AVAILABLE",
                "address_line": "Đường Nguyễn Hữu Thọ",
                "ward": "Phước Kiển",
                "district": "Nhà Bè",
                "province": "TP.HCM",
                "area_sqm": 78.5,
                "bedrooms": 2,
                "bathrooms": 2,
                "list_price": 4200000000.0,
                "published_at": datetime.now(timezone.utc),
                "images": [
                    "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1502672260266-1c1de2d96642?auto=format&fit=crop&w=600&q=80",
                    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=600&q=80"
                ]
            },
            {
                "id": uuid.uuid4(),
                "code": "L18",
                "property_kind": "LAND",
                "title": "Lô đất L18, 100 m²",
                "description": "Lô đất vuông vức L18 nằm trong khu quy hoạch đồng bộ, mặt tiền đường lớn. Thuận tiện xây dựng biệt thự hoặc nhà phố thương mại. Xung quanh đầy đủ tiện ích như trường học, siêu thị, bệnh viện.",
                "status": "AVAILABLE",
                "address_line": "Đường số 8",
                "ward": "Phước Kiển",
                "district": "Nhà Bè",
                "province": "TP.HCM",
                "area_sqm": 100.0,
                "bedrooms": 0,
                "bathrooms": 0,
                "list_price": 5000000000.0,
                "published_at": datetime.now(timezone.utc),
                "images": [
                    "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1584824486509-112e4181f1ce?auto=format&fit=crop&w=600&q=80",
                    "https://images.unsplash.com/photo-1524813686514-a57563d77200?auto=format&fit=crop&w=600&q=80"
                ]
            }
        ]

        for p_data in properties_data:
            # Check if code already exists
            result = await session.execute(text("SELECT id FROM properties WHERE code = :code"), {"code": p_data["code"]})
            existing = result.scalar()
            if existing:
                print(f"Property with code {p_data['code']} already exists. Skipping.")
                continue

            property_kind = p_data.pop("property_kind")
            status = p_data.pop("status")
            images = p_data.pop("images")
            
            await session.execute(text(f"""
                INSERT INTO properties (id, code, property_kind, title, description, status, address_line, ward, district, province, area_sqm, bedrooms, bathrooms, list_price, published_at)
                VALUES (:id, :code, '{property_kind}'::property_kind_t, :title, :description, '{status}'::property_status_t, :address_line, :ward, :district, :province, :area_sqm, :bedrooms, :bathrooms, :list_price, :published_at)
            """), p_data)
            
            for i, img_url in enumerate(images):
                await session.execute(text(f"""
                    INSERT INTO property_media (id, property_id, media_type, url, sort_order, is_cover)
                    VALUES (:id, :property_id, 'IMAGE', :url, :sort_order, :is_cover)
                """), {
                    "id": uuid.uuid4(),
                    "property_id": p_data["id"],
                    "url": img_url,
                    "sort_order": i,
                    "is_cover": (i == 0)
                })
        
        await session.commit()
        print("Successfully seeded 2 extra properties.")
        
if __name__ == "__main__":
    asyncio.run(seed())
