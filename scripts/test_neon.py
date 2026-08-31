import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def main():
    url = "postgresql+asyncpg://neondb_owner:npg_g6z9ZKivayLE@ep-winter-butterfly-b36zhphr.pooler.ap-southeast-1.aws.neon.tech/neondb?ssl=require&options=endpoint%3Dep-winter-butterfly-b36zhphr"
    try:
        print(f"Trying {url}...")
        engine = create_async_engine(url)
        async with engine.connect() as conn:
            res = await conn.execute(text("SELECT 1"))
            print(f"SUCCESS!")
            return
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(main())
