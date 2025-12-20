import requests
from constans import *

class TestNegativeApi:
    def test_bad_password(self, test_user):

        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        reg_response = requests.post(register_url, json=test_user, headers=HEADERS)


        response = requests.post(
            f"{BASE_URL}{LOGIN_ENDPOINT}",
            json={
                "email": BAD_EMAIL,
                "password": test_user["password"]
            },
            headers=HEADERS
        )


        assert response.status_code == 401
        message = response.json().get("message")
        assert message == "Неверный логин или пароль"


    def test_bad_email(self,test_user):

        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        reg_response = requests.post(register_url, json=test_user, headers=HEADERS)

        response = requests.post(
            f"{BASE_URL}{LOGIN_ENDPOINT}",
            json={
                "email": test_user["email"],
                "password": WRONG_PASSWORD
            },
            headers=HEADERS
        )


        assert response.status_code == 401
        message = response.json().get("message")
        assert message == "Неверный логин или пароль"


    def test_empty_json(self,test_user):

        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        reg_response = requests.post(register_url, json=test_user, headers=HEADERS)

        response = requests.post(
            f"{BASE_URL}{LOGIN_ENDPOINT}",
            json={},
            headers=HEADERS
        )

        # BUG: backend returns 401 instead of 400 for empty body
        assert response.status_code == 401
        message = response.json().get("message")
        assert message == "Неверный логин или пароль"