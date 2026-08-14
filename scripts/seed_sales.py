import asyncio
import uuid
import math
from random import shuffle
from sqlalchemy import select, func, delete
from src.database.connection import get_session_context
from src.database.models import User, UserRole, SaleProfile, Property, PropertySaleAssignment
from src.services.auth_service import get_password_hash

# 20 Vietnamese names
NAMES = [
    "Nguyễn Văn An", "Trần Thị Bích", "Lê Hoàng Công", "Phạm Thị Dung",
    "Hoàng Văn Ân", "Vũ Thị Hoa", "Đặng Văn Giang", "Bùi Thị Hạnh",
    "Đỗ Văn Inh", "Hồ Thị Kim", "Ngô Văn Lâm", "Dương Thị Mai",
    "Lý Văn Nam", "Đinh Thị Oanh", "Đoàn Văn Phong", "Lâm Thị Quỳnh",
    "Trịnh Văn Quân", "Mai Thị Yến", "Đào Văn Tuấn", "Phan Thị Xuân"
]

async def main():
    async with get_session_context() as session:
        # 1. Get properties by province
        city_counts = await session.execute(
            select(Property.province, func.count(Property.id))
            .where(Property.province != None)
            .group_by(Property.province)
        )
        city_counts = city_counts.all()
        total_props = sum(count for _, count in city_counts)

        print(f"Total properties with province: {total_props}")
        
        # 2. Distribute 20 sales based on ratio
        total_sales = 20
        city_sales_allocation = {}
        remaining_sales = total_sales
        
        for city, count in city_counts:
            # At least 1 sale if there's any property, otherwise proportional
            ratio = count / total_props
            allocated = max(1, math.floor(ratio * total_sales))
            if remaining_sales - allocated < 0:
                allocated = remaining_sales
            city_sales_allocation[city] = allocated
            remaining_sales -= allocated
            
        # Give remaining to the biggest city
        if remaining_sales > 0:
            biggest_city = max(city_counts, key=lambda x: x[1])[0]
            city_sales_allocation[biggest_city] += remaining_sales

        print("Sale allocation by province:", city_sales_allocation)

        # 3. Generate sales
        shuffle(NAMES)
        password_hash = get_password_hash("123456")
        name_idx = 0
        
        city_to_sale_ids = {city: [] for city in city_sales_allocation.keys()}
        
        print("Generating Sales...")
        for city, num_sales in city_sales_allocation.items():
            for _ in range(num_sales):
                sale_id = uuid.uuid4()
                full_name = NAMES[name_idx]
                # Email format: an.nv.sale@xhome.com
                parts = full_name.split()
                email = f"{parts[-1].lower()}.{''.join([p[0].lower() for p in parts[:-1]])}.sale{name_idx}@xhome.com"
                
                # Create User
                user = User(
                    id=sale_id,
                    role=UserRole.SALE,
                    email=email,
                    phone=f"+84999{name_idx:06d}",
                    password_hash=password_hash,
                    full_name=full_name,
                    email_verified_at=func.now(),
                    phone_verified_at=func.now()
                )
                session.add(user)
                
                profile = SaleProfile(
                    user_id=sale_id,
                    employee_code=f"NV-{name_idx:04d}",
                    branch_name=city,
                    job_title="Chuyên viên tư vấn"
                )
                session.add(profile)
                
                city_to_sale_ids[city].append(sale_id)
                name_idx += 1
                
        await session.flush()
        
        # 4. Clear all existing assignments and reassign
        print("Reassigning properties...")
        await session.execute(delete(PropertySaleAssignment))
        
        all_props = await session.execute(select(Property.id, Property.province))
        all_props = all_props.all()
        
        assignments = []
        for prop_id, city in all_props:
            sale_ids_for_city = city_to_sale_ids.get(city)
            if not sale_ids_for_city:
                # If a property has no city or city with no sales, pick random from biggest city
                biggest_city = max(city_counts, key=lambda x: x[1])[0]
                sale_ids_for_city = city_to_sale_ids[biggest_city]
                
            # Pick a sale round-robin or based on hash of prop_id
            sale_id = sale_ids_for_city[hash(prop_id) % len(sale_ids_for_city)]
            
            assignments.append(
                PropertySaleAssignment(
                    property_id=prop_id,
                    sale_user_id=sale_id,
                    is_primary=True,
                    assigned_at=func.now()
                )
            )
            
        session.add_all(assignments)
        await session.commit()
        
        print("Successfully generated 20 sales and assigned them to properties!")
        print("\n--- SALE ACCOUNTS (Password: 123456) ---")
        stmt = select(User).where(User.email.like('%@xhome.com'))
        res = await session.execute(stmt)
        for u in res.scalars():
            print(f"- {u.full_name}: {u.email}")

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    asyncio.run(main())
