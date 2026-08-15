import asyncio
from sqlalchemy import select, func, delete
from src.database.connection import get_session_context
from src.database.models import User, SaleProfile, Property, PropertySaleAssignment
from random import shuffle

async def main():
    async with get_session_context() as session:
        # Get properties by province
        city_counts = await session.execute(
            select(Property.province, func.count(Property.id))
            .where(Property.province != None)
            .group_by(Property.province)
        )
        city_counts = city_counts.all()
        
        # We already have 20 sales in the DB from last run
        sales = await session.execute(select(User).where(User.email.like('%@xhome.com')))
        sales = sales.scalars().all()
        
        print(f"Loaded {len(sales)} sales.")
        if len(sales) < len(city_counts):
            print("Not enough sales for all cities! But we have 20 sales and ~13 cities, should be fine.")
        
        # Distribute sales to cities ensuring at least 1 per city
        city_to_sale_ids = {city: [] for city, _ in city_counts}
        
        # Give 1 to each city
        sale_idx = 0
        for city, _ in city_counts:
            city_to_sale_ids[city].append(sales[sale_idx].id)
            # Update the SaleProfile branch_name
            profile = await session.scalar(select(SaleProfile).where(SaleProfile.user_id == sales[sale_idx].id))
            profile.branch_name = city
            session.add(profile)
            sale_idx += 1
            
        # Give remaining to Hanoi (or biggest city)
        biggest_city = max(city_counts, key=lambda x: x[1])[0]
        while sale_idx < len(sales):
            city_to_sale_ids[biggest_city].append(sales[sale_idx].id)
            profile = await session.scalar(select(SaleProfile).where(SaleProfile.user_id == sales[sale_idx].id))
            profile.branch_name = biggest_city
            session.add(profile)
            sale_idx += 1
            
        await session.flush()
        
        print("Reassigning properties...")
        await session.execute(delete(PropertySaleAssignment))
        
        all_props = await session.execute(select(Property.id, Property.province))
        all_props = all_props.all()
        
        assignments = []
        for prop_id, city in all_props:
            sale_ids_for_city = city_to_sale_ids.get(city)
            if not sale_ids_for_city:
                sale_ids_for_city = city_to_sale_ids[biggest_city]
                
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
        
        print("Successfully re-distributed sales properly across all cities!")
        for city, s_ids in city_to_sale_ids.items():
            print(f"- {city}: {len(s_ids)} sales")

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    asyncio.run(main())
