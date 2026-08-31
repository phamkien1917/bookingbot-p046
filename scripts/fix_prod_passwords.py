import asyncio
import asyncpg
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.services.auth_service import get_password_hash

async def main():
    url = "postgresql://neondb_owner:npg_g6z9ZKivayLE@ep-winter-butterfly-b36zhnhr-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb"
    try:
        print(f"Connecting to production DB...")
        conn = await asyncpg.connect(url, ssl="require")
        
        valid_hash = get_password_hash("Demo@123")
        
        users = await conn.fetch("SELECT id, email FROM users WHERE password_hash = 'DEMO_ONLY_REPLACE_WITH_ARGON2ID_HASH'")
        
        print(f"Found {len(users)} users with invalid passwords.")
        
        for user in users:
            await conn.execute("UPDATE users SET password_hash = $1 WHERE id = $2", valid_hash, user['id'])
            print(f"Updated password for: {user['email']}")
            
        await conn.close()
        print("Passwords fixed on production successfully!")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(main())
