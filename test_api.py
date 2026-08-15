import asyncio
import asyncpg
import json

async def run():
    conn = await asyncpg.connect('postgresql://postgres:123@localhost:5432/test_db')
    
    users = []
    
    rows = await conn.fetch("SELECT full_name, email, role FROM users ORDER BY role DESC, email ASC")
    for r in rows:
        users.append({
            "name": r['full_name'],
            "email": r['email'],
            "role": r['role']
        })
        
    with open('users_dump.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

asyncio.run(run())
