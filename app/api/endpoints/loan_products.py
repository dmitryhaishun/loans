from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.api import deps
from app.crud import crud_loan_product
from app.models import LoanProduct
from app.schemas.base import Pagination

api = APIRouter()


@api.get("/", response_model=list[schemas.loan_products.GetLoanProductSchema])
async def get_all_loan_products(
    pagination: Pagination = Depends(), session: AsyncSession = Depends(deps.get_db)
) -> list[LoanProduct]:
    loan_products = await crud_loan_product.loan_product.get_multi(
        pagination.offset, pagination.limit, session
    )
    return loan_products


@api.get(
    "/{loan_product_id}/", response_model=schemas.loan_products.GetLoanProductSchema
)
async def get_loan_product(
    data: schemas.loan_products.GetOneLoanProductSchema = Depends(),
    session: AsyncSession = Depends(deps.get_db),
) -> LoanProduct:
    loan_product = await crud_loan_product.loan_product.get(
        session, data.loan_product_id
    )

    if not loan_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Loan product not found"
        )

    return loan_product
