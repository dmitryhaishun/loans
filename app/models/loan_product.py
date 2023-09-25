from sqlalchemy import ARRAY, DECIMAL, Column, Enum, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.utils import LoanCurrency, LoanProductType


class LoanProduct(Base):
    __tablename__ = "loan_products"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum(LoanProductType), nullable=False)
    description = Column(String, nullable=False)
    loan_amount = Column(ARRAY(Integer), nullable=False)
    loan_term = Column(ARRAY(Integer), nullable=False)
    apr = Column(DECIMAL, nullable=False)

    loans = relationship("Loan", back_populates="loan_product")

    @hybrid_property
    def currency(self):
        return [LoanCurrency.USD, LoanCurrency.EUR]
