import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Loan


def generate_number():
    return str(random.randint(0, 9999999999999999)).zfill(16)


async def create_loan_contract_number(session: AsyncSession) -> str:
    """

    Creates a unique loan contract number
    """
    query = select(Loan.loan_contract_number)
    result = await session.execute(query)
    existing_contract_numbers = [row for row in result.scalars()]
    generated_number = generate_number()
    while generated_number in existing_contract_numbers:
        generated_number = generate_number()
    return generated_number


def get_next_payment_date() -> str:
    return (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")
