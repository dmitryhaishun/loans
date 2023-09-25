from app.crud.base import CRUDBase
from app.models import LoanProduct
from app.schemas.loan_products import LoanProductCreate, LoanProductUpdate


class CRUDLoanProduct(CRUDBase[LoanProduct, LoanProductCreate, LoanProductUpdate]):
    pass


loan_product = CRUDLoanProduct(LoanProduct)
