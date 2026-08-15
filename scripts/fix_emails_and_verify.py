import asyncio
import unicodedata
from sqlalchemy import select, func, delete, update
from src.database.connection import get_session_context
from src.database.models import User, SaleProfile, Property, PropertySaleAssignment

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).replace('đ', 'd').replace('Đ', 'D')

async def main():
    async with get_session_context() as session:
        # 1. Fix emails
        sales = await session.execute(select(User).where(User.email.like('%@xhome.com')))
        sales = sales.scalars().all()
        for sale in sales:
            old_email = sale.email
            new_email = remove_accents(old_email)
            if old_email != new_email:
                sale.email = new_email
                session.add(sale)
        
        await session.flush()
        
        # 2. Check Da Nang properties and their assigned sales
        danang_props = await session.execute(
            select(Property.id, Property.title, User.full_name)
            .join(PropertySaleAssignment, PropertySaleAssignment.property_id == Property.id)
            .join(User, User.id == PropertySaleAssignment.sale_user_id)
            .where(Property.province == 'Đà Nẵng')
        )
        print("Đà Nẵng Properties:")
        for prop_id, title, sale_name in danang_props.all():
            print(f"- {title}: assigned to {sale_name}")

        # Check Ha Noi properties
        hanoi_props = await session.execute(
            select(Property.id, Property.title, User.full_name)
            .join(PropertySaleAssignment, PropertySaleAssignment.property_id == Property.id)
            .join(User, User.id == PropertySaleAssignment.sale_user_id)
            .where(Property.province == 'Hà Nội')
            .limit(5)
        )
        print("\nHà Nội Properties (first 5):")
        for prop_id, title, sale_name in hanoi_props.all():
            print(f"- {title}: assigned to {sale_name}")

        await session.commit()
        print("\nFixed emails successfully!")

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    asyncio.run(main())
