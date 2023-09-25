import asyncio
import datetime
from decimal import Decimal
from typing import AsyncGenerator

import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import app.models as models
from app.api.deps import get_db
from app.core.config import settings
from app.db.session import Base
from app.main import app
from app.utils import LoanCurrency, LoanProductType, LoanStage, LoanStatus

load_dotenv()

test_db = settings.SQLALCHEMY_TEST_DATABASE_URI

engine = create_async_engine(test_db, poolclass=NullPool)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = test_db


async def override_get_async_session():
    async with async_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_async_session


@pytest_asyncio.fixture(autouse=True, scope="function")
async def prepare_database() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def add_loan_products():
    async with async_session() as session:
        loan_product_1 = insert(models.LoanProduct).values(
            id=1,
            type=LoanProductType.STUDENT_LOAN,
            description="A loan for students",
            loan_amount={5000, 300000, 525000, 750000},
            loan_term={31536000, 157680000, 473040000},
            apr=Decimal("7.1"),
        )
        loan_product_2 = insert(models.LoanProduct).values(
            id=2,
            type=LoanProductType.AUTO_LOAN,
            description="A loan for buying cars",
            loan_amount={5000, 300000, 525000, 750000},
            loan_term={31536000, 157680000, 473040000},
            apr=Decimal("2"),
        )
        loan_product_3 = insert(models.LoanProduct).values(
            id=3,
            type=LoanProductType.MORTGAGE_LOAN,
            description="A loan for buying a house",
            loan_amount={5000, 300000, 525000, 750000},
            loan_term={31536000, 157680000, 473040000},
            apr=Decimal("3.9"),
        )

        await session.execute(loan_product_1)
        await session.execute(loan_product_2)
        await session.execute(loan_product_3)
        await session.commit()

        return [loan_product_1, loan_product_2, loan_product_3]


@pytest_asyncio.fixture
async def add_loan(add_loan_products):
    async with async_session() as session:
        loan_1 = insert(models.Loan).values(
            user_uuid="48629f80-77cc-4482-ac86-f8ba96348133",
            fk_loans_loan_products=1,
            loan_contract_number="1111111111111111",
            amount=100,
            currency=LoanCurrency.USD,
            stage=LoanStage.NONE,
            loan_term=datetime.timedelta(weeks=52),
            loan_status=LoanStatus.ACTIVE,
            loan_guarantors="John Doe",
            application_date=datetime.date.today(),
            updated_at=datetime.date.today(),
            apr=Decimal("5.1"),
            paid_amount=0,
        )
        loan_2 = insert(models.Loan).values(
            user_uuid="48629f80-77cc-4482-ac86-f8ba96348133",
            fk_loans_loan_products=2,
            loan_contract_number="2222222222222222",
            amount=100,
            currency=LoanCurrency.USD,
            stage=LoanStage.NONE,
            loan_term=datetime.timedelta(weeks=52),
            loan_status=LoanStatus.DEBT,
            loan_guarantors="John Doe",
            application_date=datetime.date.today(),
            updated_at=datetime.date.today(),
            apr=Decimal("5.1"),
            paid_amount=0,
        )
        loan_3 = insert(models.Loan).values(
            user_uuid="48629f80-77cc-4482-ac86-f8ba96348133",
            fk_loans_loan_products=3,
            loan_contract_number="3333333333333333",
            amount=100,
            currency=LoanCurrency.USD,
            stage=LoanStage.NONE,
            loan_term=datetime.timedelta(weeks=52),
            loan_status=LoanStatus.PAID_OFF,
            loan_guarantors="John Doe",
            application_date=datetime.date.today(),
            updated_at=datetime.date.today(),
            apr=Decimal("5.1"),
            paid_amount=0,
        )

        await session.execute(loan_1)
        await session.execute(loan_2)
        await session.execute(loan_3)
        await session.commit()
