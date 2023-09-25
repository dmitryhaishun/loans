from datetime import date, timedelta

from fastapi import Query
from pydantic import BaseModel, Field, condecimal

from app.schemas.base import DBBase, IDSchema, Pagination, UUIDSchema
from app.utils import LoanCurrency, LoanProductType, LoanStage, LoanStatus, LoanType


class LoanBaseSchema(BaseModel):
    loan_contract_number: str | None = Field(example="ABC123")
    amount: condecimal(ge=0, decimal_places=2) = Field(example="10000.00")  # type: ignore # noqa
    currency: LoanCurrency
    loan_term: timedelta = Field(example=31536000)
    loan_status: LoanStatus
    loan_guarantors: str | None = Field(example="John Doe")
    apr: condecimal(ge=0, decimal_places=2) = Field(example="5.25")  # type: ignore # noqa


class LoanTypeSchema(BaseModel):
    type: LoanProductType


class LoanDynamicFields(BaseModel):
    remaining_amount: condecimal(ge=0, decimal_places=2) = Field(example="2500.00")  # type: ignore # noqa
    next_payment_date: date = Field(example="2023-10-01")
    next_payment_amount: condecimal(ge=0, decimal_places=2) = Field(example="1000.00")  # type: ignore # noqa
    progress_circle: condecimal(ge=0, decimal_places=2) = Field(example="75.00")  # type: ignore # noqa


class GetLoanSchema(
    LoanDynamicFields, LoanBaseSchema, LoanTypeSchema, UUIDSchema, IDSchema, DBBase
):
    loan_type_id: int = Field(example=1)
    stage: LoanStage
    application_date: date = Field(example="2023-09-01")
    updated_at: date = Field(example="2023-09-06")
    paid_amount: condecimal(ge=0, decimal_places=2) = Field(example="7500.00")  # type: ignore # noqa
    last_payment_date: date | None = Field(example="2023-08-01")


class GetAllLoansRequestSchema(UUIDSchema, Pagination):
    loan_type: LoanType | None


class GetOneLoanSchema(UUIDSchema):
    loan_id: int = Query(default=1, ge=1)


class LoanApplicationSchema(LoanBaseSchema, LoanTypeSchema, IDSchema, DBBase):
    stage: LoanStage
    application_date: date = Field(example="2023-09-01")


class LoanSchema(LoanDynamicFields, LoanBaseSchema, LoanTypeSchema, IDSchema, DBBase):
    pass


class LoanCreateSchema(DBBase, LoanBaseSchema, UUIDSchema):
    loan_type_id: int = Field(example=1)
    stage: LoanStage
    application_date: date = Field(example="2023-09-01")


class LoanUpdateSchema(LoanCreateSchema):
    pass


class LoanCreateIncomingSchema(DBBase, UUIDSchema):
    loan_type_id: int = Field(example=1)
    amount: condecimal(ge=0, decimal_places=2) = Field(example="10000.00")  # type: ignore # noqa
    loan_term: timedelta = Field(example=31536000)
    currency: LoanCurrency
    loan_guarantors: str | None = Field(example="John Doe")
    apr: condecimal(ge=0, decimal_places=2) = Field(example="5.25")  # type: ignore # noqa
