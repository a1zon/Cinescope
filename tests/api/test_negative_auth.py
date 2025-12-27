from constants import WRONG_PASSWORD,BAD_EMAIL
from api.api_manager import ApiManager

class TestNegativeApi:

    def test_bad_password(self, api_manager: ApiManager, test_user):
        """"
        Логин с неправильным паролем
        """

        data={
                "email": test_user["email"],
                "password": WRONG_PASSWORD
            },
        response = api_manager.auth_api.login_user(data,expected_status=401,)
        assert response.status_code == 401
        message = response.json().get("message")
        assert message == "Неверный логин или пароль"

    def test_bad_email(self,api_manager: ApiManager, test_user):
        """"
        Логин с неправильным email
        """
        data={
                "email": BAD_EMAIL,
                "password": test_user["password"]
            },
        response = api_manager.auth_api.login_user(data,expected_status=401,)
        assert response.status_code == 401
        message = response.json().get("message")
        assert message == "Неверный логин или пароль"

    def test_empty_json(self,api_manager: ApiManager, test_user):
        """"
        Логин с пустым json
        """
        data={}
        response = api_manager.auth_api.login_user(data,expected_status=401,)
        assert response.status_code == 401
        message = response.json().get("message")
        assert message == "Неверный логин или пароль"