import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database import async_session_maker

async def delete_fake():
    async with async_session_maker() as session:
        codes = ['SR-A1208', 'SR-L18', 'A-1208', 'L18']
        
        # Get IDs
        result = await session.execute(text("SELECT id FROM properties WHERE code = ANY(:codes)"), {"codes": codes})
        property_ids = [row[0] for row in result.fetchall()]
        
        if property_ids:
            print(f"Found fake properties with IDs: {property_ids}")
            
            # Delete dependent records
            try:
                await session.execute(text("DELETE FROM tour_requests WHERE property_id = ANY(:ids)"), {"ids": property_ids})
            except Exception as e:
                print(f"Ignore tour_requests error: {e}")
                
            try:
                await session.execute(text("DELETE FROM property_media WHERE property_id = ANY(:ids)"), {"ids": property_ids})
            except Exception as e:
                print(f"Ignore property_media error: {e}")
                
            # Delete properties
            await session.execute(text("DELETE FROM properties WHERE id = ANY(:ids)"), {"ids": property_ids})
            
            await session.commit()
            print("Successfully deleted fake properties.")
        else:
            print("No fake properties found.")

if __name__ == "__main__":
    asyncio.run(delete_fake())
