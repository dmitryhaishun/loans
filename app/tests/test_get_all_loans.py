from httpx import AsyncClient
from starlette import status

LOAN_URL = "/loans/"
LOAN_URL_BY_ID = "/loans/{loan_id}/"


class TestGetLoans:
    async def test_all_loans(self, ac: AsyncClient, add_loan, add_loan_products):
        json = {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "limit": "100",
            "offset": "0",
            "loan_type": "loans",
        }
        response = await ac.post(LOAN_URL, json=json)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    async def test_all_loans2(self, ac: AsyncClient, add_loan, add_loan_products):
        json = {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "limit": "100",
            "offset": "0",
            "loan_type": "applications",
        }
        response = await ac.post(LOAN_URL, json=json)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    async def test_invalid_user_uuid(self, ac: AsyncClient):
        request_body = {
            "user_uuid": "invalid-uuid",
            "limit": "100",
            "offset": "0",
            "loan_type": "Loans",
        }

        response = await ac.post(LOAN_URL, json=request_body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body", "user_uuid"]
        assert response.json()["detail"][0]["type"] == "type_error.uuid"

    async def test_invalid_loan_type(self, ac: AsyncClient):
        request_body = {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "limit": "100",
            "offset": "0",
            "loan_type": "invalid-loan-type",
        }

        response = await ac.post(LOAN_URL, json=request_body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body", "loan_type"]
        assert response.json()["detail"][0]["type"] == "type_error.enum"

    async def test_invalid_offset(self, ac: AsyncClient):
        request_body = {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "limit": "100",
            "offset": "-1",
            "loan_type": "Loans",
        }

        response = await ac.post(LOAN_URL, json=request_body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body", "offset"]
        assert response.json()["detail"][0]["type"] == "value_error.number.not_ge"

    async def test_invalid_limit(self, ac: AsyncClient):
        request_body = {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "limit": "-1",
            "offset": "0",
            "loan_type": "Loans",
        }

        response = await ac.post(LOAN_URL, json=request_body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body", "limit"]
        assert response.json()["detail"][0]["type"] == "value_error.number.not_ge"

    async def test_no_request_body(self, ac: AsyncClient):
        response = await ac.post(LOAN_URL)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body"]
        assert response.json()["detail"][0]["type"] == "value_error.missing"

    async def test_empty_data_in_request_body(self, ac: AsyncClient):
        request_body: dict[str, str] = {}
        response = await ac.post(LOAN_URL, json=request_body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body", "user_uuid"]
        assert response.json()["detail"][0]["type"] == "value_error.missing"

    async def test_invalid_data_in_request_body(self, ac: AsyncClient):
        request_body = {
            "user_uuid": "invalid-uuid",
            "limit": "invalid-limit",
            "offset": "invalid-offset",
            "loan_type": "invalid-loan-type",
        }
        response = await ac.post(LOAN_URL, json=request_body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetOneLoan:
    async def test_loan_by_id_success(self, ac: AsyncClient, add_loan):
        request_body = {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "loan_id": 3,
        }

        response = await ac.post(LOAN_URL_BY_ID, json=request_body)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    async def test_loan_by_id_fail(self, ac: AsyncClient, add_loan):
        request_body = {
            "user_uuid": "48629f80-77cc-4482-ac86-f8ba96348133",
            "loan_id": 4,
        }

        response = await ac.post(LOAN_URL_BY_ID, json=request_body)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Loan with id 4 not found"

    async def test_loan_by_id_invalid_uuid(self, ac: AsyncClient):
        request_body = {"user_uuid": "invalid-uuid", "loan_id": 1}

        response = await ac.post(LOAN_URL_BY_ID, json=request_body)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["loc"] == ["body", "user_uuid"]
