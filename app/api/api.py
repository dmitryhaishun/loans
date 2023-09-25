from fastapi import APIRouter

from app.api.endpoints import loan_products, loans

api = APIRouter()

api.include_router(loans.api, tags=["Loans"], prefix="/loans")
api.include_router(loan_products.api, tags=["Loan Products"], prefix="/products")
