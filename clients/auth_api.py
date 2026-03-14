import requests

from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.requestor import CustomRequester


class AuthApi(CustomRequester):
    """Клиент для работы с Auth API (регистрация, логин, токены)."""

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    @staticmethod
    def get_user_token(response: requests.Response) -> str:
        """Извлекает accessToken из ответа сервера."""
        data = response.json()
        if "accessToken" not in data:
            raise KeyError("accessToken отсутствует в ответе сервера")
        return data["accessToken"]

    def register_user(self, user_data: dict, expected_status=201) -> requests.Response:
        """Регистрация нового пользователя."""
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data: dict, expected_status=200) -> requests.Response:
        """Авторизация пользователя (получение JWT-токена)."""
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user: dict) -> None:
        """Выполняет логин и сохраняет Bearer-токен в заголовки сессии."""
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        response = self.login_user(login_data)
        token = self.get_user_token(response)
        self._update_session_headers(**{"authorization": f"Bearer {token}"})

    def authenticate_admin(self) -> None:
        """Логин под учётной записью администратора (креды из .env)."""
        login_data = {
            "email": "api1@gmail.com",
            "password": "asdqwe123Q"
        }
        response = self.login_user(login_data)
        token = self.get_user_token(response)
        self._update_session_headers(**{"authorization": f"Bearer {token}"})
