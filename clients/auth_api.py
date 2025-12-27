import requests
from constants import  REGISTER_ENDPOINT, LOGIN_ENDPOINT
from  custom_requester.requestor import  CustomRequester
from constants import BASE_URL

class AuthApi(CustomRequester):
    """
    класс для работы с аунтефикацией
    """
    
    def __init__(self,session):
        super().__init__(session=session, base_url=BASE_URL)

    @staticmethod
    def get_user_token( response: requests.Response):
        data = response.json()
        if "accessToken" not in data:
            raise KeyError("token is missing")
        token = data["accessToken"]
        return token

    def register_user(self,user_data,expected_status = 201) -> requests.Response:
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )


    def login_user(self, login_data, expected_status=201) -> requests.Response:
        """
        Авторизация пользователя.
        :param login_data: Данные для логина
        :param expected_status: Ожидаемый статус-код
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )


    def authenticate(self, user) -> None:
        """
        Логин обчного юзера
        """
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }

        response = self.login_user(login_data)

        token = self.get_user_token(response)


        self._update_session_headers(**{"authorization": "Bearer " + token})

    def authenticate_admin(self) -> None:
        """
        Логин админа
        """
        login_data = {
            "email": "api1@gmail.com",
            "password": "asdqwe123Q"
        }

        response = self.login_user(login_data)

        token = self.get_user_token(response)

        self._update_session_headers(**{"authorization": "Bearer " + token})

