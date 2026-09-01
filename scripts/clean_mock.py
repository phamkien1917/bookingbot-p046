import asyncio
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select

from src.database.connection import get_session_context
from src.database.models import Property, PropertyMedia, PropertySaleAssignment


async def main():
    async with get_session_context() as session:
        # Revert properties created in the last 20 minutes
        cutoff_time = datetime.now(UTC) - timedelta(minutes=20)

        stmt = select(Property.id).where(Property.created_at >= cutoff_time)
        result = await session.execute(stmt)
        prop_ids = result.scalars().all()

        if not prop_ids:
            print("No recently created properties found.")
            return

        print(f"Found {len(prop_ids)} properties to revert.")

        # We need to revert assignments and media first
        await session.execute(delete(PropertySaleAssignment).where(PropertySaleAssignment.property_id.in_(prop_ids)))
        await session.execute(delete(PropertyMedia).where(PropertyMedia.property_id.in_(prop_ids)))

        # Now revert the properties
        await session.execute(delete(Property).where(Property.id.in_(prop_ids)))

        await session.commit()
        print(f"Successfully reverted {len(prop_ids)} mock properties!")

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    asyncio.run(main())
