from httpx import AsyncClient
from starlette import status

LOAN_PRODUCTS_URL = "/products/"
LOAN_PRODUCT_BY_ID_URL = "/products/{loan_product_id}/"


class TestGetLoanProducts:
    async def test_get_all_loan_products(self, ac: AsyncClient, add_loan_products):
        response = await ac.get(LOAN_PRODUCTS_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    async def test_get_loan_product_success(self, ac: AsyncClient, add_loan_products):
        response = await ac.get(LOAN_PRODUCT_BY_ID_URL.format(loan_product_id=1))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    async def test_get_loan_product_fail(self, ac: AsyncClient, add_loan_products):
        response = await ac.get(LOAN_PRODUCT_BY_ID_URL.format(loan_product_id=4))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Loan product not found"
