from datetime import date, timedelta
from math import floor

from pydantic.types import Decimal
from sqlalchemy import (
    DECIMAL,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    Interval,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.utils import LoanCurrency, LoanStage, LoanStatus


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, nullable=False)
    user_uuid = Column(UUID(as_uuid=True), nullable=False)
    loan_type_id = Column(
        Integer,
        ForeignKey("loan_products.id"),
        nullable=False,
        name="fk_loans_loan_products",
    )
    loan_contract_number = Column(String, nullable=False, unique=True)
    amount = Column(Integer, nullable=False)
    currency = Column(Enum(LoanCurrency), nullable=False)
    stage = Column(Enum(LoanStage), nullable=True)
    loan_term = Column(Interval, nullable=False)
    loan_status = Column(Enum(LoanStatus), nullable=False)
    loan_guarantors = Column(String, nullable=True)
    application_date = Column(Date, default=date.today, nullable=False)
    updated_at = Column(Date, nullable=True)
    last_payment_date = Column(Date, nullable=True)
    apr = Column(DECIMAL, nullable=False)
    paid_amount = Column(DECIMAL, nullable=True)

    loan_product = relationship("LoanProduct", back_populates="loans")

    @hybrid_property
    def type(self):
        return self.loan_product.type

    @hybrid_property
    def remaining_amount(self):
        return self.amount - self.paid_amount

    @hybrid_property
    def next_payment_date(self):
        if self.last_payment_date:
            return self.last_payment_date + timedelta(days=30)
        else:
            return self.updated_at + timedelta(days=30)

    @hybrid_property
    def next_payment_amount(self):
        return round(
            self.amount
            / (Decimal(str(self.loan_term.total_seconds())) / (24 * 60 * 60 * 30)),
            2,
        )

    @hybrid_property
    def progress_circle(self):
        return floor(self.paid_amount / self.amount * 100)
