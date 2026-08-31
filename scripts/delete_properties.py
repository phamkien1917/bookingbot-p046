import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, delete
from src.database.connection import get_session_context
from src.database.models import Property, PropertyMedia, PropertySaleAssignment

async def main():
    async with get_session_context() as session:
        # Delete properties created in the last 20 minutes
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=20)
        
        stmt = select(Property.id).where(Property.created_at >= cutoff_time)
        result = await session.execute(stmt)
        prop_ids = result.scalars().all()
        
        if not prop_ids:
            print("No recently created properties found.")
            return
            
        print(f"Found {len(prop_ids)} properties to delete.")
        
        # We need to delete assignments and media first
        await session.execute(delete(PropertySaleAssignment).where(PropertySaleAssignment.property_id.in_(prop_ids)))
        await session.execute(delete(PropertyMedia).where(PropertyMedia.property_id.in_(prop_ids)))
        
        # Now delete the properties
        await session.execute(delete(Property).where(Property.id.in_(prop_ids)))
        
        await session.commit()
        print(f"Successfully deleted {len(prop_ids)} mock properties!")

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    asyncio.run(main())
