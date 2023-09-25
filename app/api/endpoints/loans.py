from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.api import deps
from app.crud import crud_loan
from app import models, schemas

api = APIRouter()


@api.post("/create")
async def create_new_loan(
    data: schemas.loan.LoanCreateIncomingSchema,
    session: AsyncSession = Depends(deps.get_db)
) -> JSONResponse:

    try:
        await crud_loan.loan.create_loan(session, data=data)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Loan application has been made"})
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error while creating loan")


@api.post(
    "/",
    response_model=list[
        schemas.loan.GetLoanSchema
        | schemas.loan.LoanSchema
        | schemas.loan.LoanApplicationSchema
    ],
)
async def get_all_loans(
    data: schemas.loan.GetAllLoansRequestSchema,
    session: AsyncSession = Depends(deps.get_db),
) -> list[models.Loan]:
    loans = await crud_loan.loan.get_multi_with_filter(
        session, data.user_uuid, data.loan_type, data.offset, data.limit
    )
    return loans  # type: ignore[return-value]


@api.post(
    "/{loan_id}/",
    response_model=schemas.loan.GetLoanSchema
    | schemas.loan.LoanSchema
    | schemas.loan.LoanApplicationSchema,
)
async def get_loan(
    data: schemas.loan.GetOneLoanSchema, session: AsyncSession = Depends(deps.get_db)
) -> models.Loan:
    loan = await crud_loan.loan.get_one_loan(session, data.loan_id, data.user_uuid)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan with id {data.loan_id} not found",
        )
    return loan
