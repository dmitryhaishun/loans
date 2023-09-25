from fastapi import Query
from pydantic import BaseModel, Field, condecimal

from app.schemas.base import DBBase
from app.utils import LoanCurrency, LoanProductType


class LoanProductBaseSchema(BaseModel):
    type: LoanProductType = Field(example=LoanProductType.STUDENT_LOAN)
    description: str = Field(example="A loan for students")
    loan_amount: list = Field(example=[5000, 300000, 525000, 750000])
    loan_term: list = Field(example=[31536000, 157680000, 473040000])
    apr: condecimal(gt=0, decimal_places=2) = Field(example=6.02)  # type: ignore


class GetLoanProductSchema(DBBase, LoanProductBaseSchema):
    currency: list = Field(example=[LoanCurrency.USD, LoanCurrency.EUR])


class GetOneLoanProductSchema(BaseModel):
    loan_product_id: int = Query(default=1, ge=1)


class LoanProductCreate(LoanProductBaseSchema):
    pass


class LoanProductUpdate(LoanProductBaseSchema):
    pass
