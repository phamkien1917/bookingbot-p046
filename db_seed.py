import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from src.database import async_session_maker, engine
from src.models import Property, PropertyMedia
from datetime import datetime, timezone

async def seed():
    async with async_session_maker() as session:
        # Xóa dữ liệu cũ
        await session.execute(delete(Property))
        
        # Dữ liệu mẫu
        properties_data = [
            {
                "id": uuid.uuid4(),
                "code": "VH-CP-204",
                "property_kind": "APARTMENT",
                "title": "Căn hộ cao cấp Vinhomes Central Park",
                "description": "Căn hộ tọa lạc tại tầng 15 của tòa tháp, mang đến tầm nhìn toàn cảnh ra sông Sài Gòn tuyệt đẹp. Thiết kế nội thất theo phong cách Minimalism hiện đại. Hệ thống smarthome tích hợp giúp quản lý năng lượng và an ninh hiệu quả.",
                "status": "AVAILABLE",
                "address_line": "208 Nguyễn Hữu Cảnh",
                "ward": "Phường 22",
                "district": "Bình Thạnh",
                "province": "TP.HCM",
                "area_sqm": 75.0,
                "bedrooms": 2,
                "bathrooms": 2,
                "list_price": 4500000000.0,
                "published_at": datetime.now(timezone.utc),
                "images": [
                    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1600607687931-ce71171f1e73?auto=format&fit=crop&w=600&q=80",
                    "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=600&q=80"
                ]
            },
            {
                "id": uuid.uuid4(),
                "code": "RIV-T1-10",
                "property_kind": "APARTMENT",
                "title": "The River Thủ Thiêm - Tháp Seine",
                "description": "Căn hộ hạng sang The River Thủ Thiêm 2PN, view trực diện Landmark 81.",
                "status": "AVAILABLE",
                "address_line": "Đại lộ Vòng Cung",
                "ward": "Thủ Thiêm",
                "district": "Quận 2",
                "province": "TP.HCM",
                "area_sqm": 85.0,
                "bedrooms": 2,
                "bathrooms": 2,
                "list_price": 4500000000.0,
                "published_at": datetime.now(timezone.utc),
                "images": [
                    "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1502672260266-1c1de2d96642?auto=format&fit=crop&w=600&q=80"
                ]
            },
            {
                "id": uuid.uuid4(),
                "code": "EMP-LD-12",
                "property_kind": "APARTMENT",
                "title": "Empire City - Linden Residences",
                "description": "Căn hộ Empire City Linden Residences, diện tích lớn, thiết kế đẳng cấp, tiện ích vượt trội.",
                "status": "AVAILABLE",
                "address_line": "Đường Mai Chí Thọ",
                "ward": "Thủ Thiêm",
                "district": "Quận 2",
                "province": "TP.HCM",
                "area_sqm": 110.0,
                "bedrooms": 3,
                "bathrooms": 2,
                "list_price": 6200000000.0,
                "published_at": datetime.now(timezone.utc),
                "images": [
                    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=600&q=80"
                ]
            },
            {
                "id": uuid.uuid4(),
                "code": "NP-D7-01",
                "property_kind": "HOUSE",
                "title": "Nhà phố liền kề Quận 7 - Him Lam",
                "description": "Nhà phố Khu dân cư Him Lam Tân Hưng. Thiết kế sang trọng.",
                "status": "AVAILABLE",
                "address_line": "Đường số 10",
                "ward": "Tân Hưng",
                "district": "Quận 7",
                "province": "TP.HCM",
                "area_sqm": 100.0,
                "bedrooms": 4,
                "bathrooms": 4,
                "list_price": 12000000000.0,
                "published_at": datetime.now(timezone.utc),
                "images": [
                    "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80",
                    "https://images.unsplash.com/photo-1600040913982-1681283c7490?auto=format&fit=crop&w=600&q=80"
                ]
            },
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
            images = p_data.pop("images")
            prop = Property(**p_data)
            session.add(prop)
            for i, img_url in enumerate(images):
                media = PropertyMedia(
                    property_id=prop.id,
                    media_type="IMAGE",
                    url=img_url,
                    sort_order=i,
                    is_cover=(i==0)
                )
                session.add(media)
        
        await session.commit()
        print("Successfully seeded 4 properties.")
        
if __name__ == "__main__":
    asyncio.run(seed())
