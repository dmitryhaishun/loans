from datetime import date

from pydantic import parse_obj_as
from pydantic.types import UUID
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

import app.utils
from app.crud.base import CRUDBase
from app.crud.utils import create_loan_contract_number
from app.models import Loan, LoanProduct
from app.schemas.loan import (
    LoanApplicationSchema,
    LoanCreateIncomingSchema,
    LoanCreateSchema,
    LoanSchema,
    LoanUpdateSchema,
)
from app.utils import LoanStage, LoanStatus, LoanType


class CRUDLoan(CRUDBase[Loan, LoanCreateSchema, LoanUpdateSchema]):
    async def get_multi_with_filter(
        self,
        session: AsyncSession,
        user_uuid: UUID,
        loans_type: LoanType | None,
        offset: int | None,
        limit: int | None,
    ) -> list[Loan | LoanSchema | LoanApplicationSchema]:

        base_query = (
            select(self.model)
            .join(LoanProduct)
            .options(joinedload(self.model.loan_product))
            .where(self.model.user_uuid == user_uuid)
        )

        if loans_type == LoanType.LOANS:
            base_query = (
                base_query.where(self.model.loan_status.in_(app.utils.loan_statuses))
                .offset(offset)
                .limit(limit)
                .order_by(self.model.loan_status)
            )
            result = await session.execute(base_query)
            loans = parse_obj_as(list[LoanSchema], result.scalars().all())
            return loans  # type: ignore[return-value]
        elif loans_type == LoanType.LOAN_APPLICATIONS:
            base_query = (
                base_query.where(
                    self.model.loan_status.in_(app.utils.loan_application_statuses)
                )
                .offset(offset)
                .limit(limit)
                .order_by(self.model.loan_status)
            )
            query = (
                base_query.offset(offset).limit(limit).order_by(self.model.loan_status)
            )
            result = await session.execute(query)
            loans = parse_obj_as(
                list[LoanApplicationSchema], result.scalars().all()  # type: ignore[arg-type] # noqa: E501
            )
            return loans  # type: ignore[return-value]

        query = base_query.offset(offset).limit(limit).order_by(self.model.loan_status)
        loans = await session.execute(query)
        return loans.scalars().all()  # type: ignore[attr-defined]

    async def get_one_loan(  # type: ignore[return]
        self, session: AsyncSession, id: int, user_uuid: UUID
    ) -> Loan:
        query = (
            select(self.model)
            .join(LoanProduct)
            .options(joinedload(self.model.loan_product))
            .where(and_(self.model.user_uuid == user_uuid), self.model.id == id)
        )

        result = await session.execute(query)
        one_loan = result.scalars().first()

        if one_loan:
            if one_loan.loan_status in app.utils.loan_application_statuses:
                loan = parse_obj_as(
                    LoanApplicationSchema, one_loan
                )  # type: ignore[assignment]
                return loan  # type: ignore[return-value]

            elif one_loan.loan_status in app.utils.loan_statuses:
                loan = parse_obj_as(LoanSchema, one_loan)  # type: ignore[assignment]
                return loan  # type: ignore[return-value]

            else:
                return one_loan

    async def create_loan(
        self, session: AsyncSession, *, data: LoanCreateIncomingSchema
    ) -> str:
        loan_contract_number = await create_loan_contract_number(session)

        new_data = LoanCreateSchema(
            user_uuid=data.user_uuid,
            loan_type_id=data.loan_type_id,
            loan_contract_number=loan_contract_number,
            amount=data.amount,
            currency=data.currency,
            stage=LoanStage.NONE,
            loan_term=data.loan_term,
            loan_status=LoanStatus.DRAFT,
            loan_guarantors=data.loan_guarantors,
            application_date=date.today(),
            apr=data.apr,
        )

        new_loan = await self.create(session, data=new_data)
        return new_loan


loan = CRUDLoan(Loan, LoanProduct)
