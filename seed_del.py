import asyncio

from app.db.session import get_or_create_engine, get_or_create_session


async def clear_table_data() -> None:
    async with get_or_create_session() as session:
        await session.execute("TRUNCATE TABLE loans, loan_products RESTART IDENTITY")
        await session.commit()
        print("DELETED")


if __name__ == "__main__":
    get_or_create_engine()
    asyncio.run(clear_table_data())
