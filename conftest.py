import  requests
from constans import *
import pytest
from utils.data_generator import DataGenerator
from custom_requester.requestor import CustomRequester

@pytest.fixture(scope = "session")
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

# @pytest.fixture(scope = "session")
# def auth_session(test_user):
#     reg_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
#     response = requests.post(reg_url, json= test_user, headers= HEADERS)
#     assert response.status_code == 201, "Ошибка регистрации пользователя"
#
#     login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'
#     login_data = {
#         "email": test_user["email"],
#         "password": test_user["password"]
#     }
#     response = requests.post(login_url, json=login_data, headers=HEADERS)
#     assert response.status_code == 200, "Ошибка авторизации"
#
#     token = response.json().get("accessToken")
#     assert token is not None, "Токен доступа отсутствует в ответе"
#
#     session = requests.Session()
#     session.headers.update(HEADERS)
#     session.headers.update({"Authorization": f"Bearer {token}"})
#     return session

@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request( # а вот эта строчка как вообще работает? - в фистуре ведь нету некакого метода send request - откуда питон его берет и почему мы можем вызывать его так ?
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)
