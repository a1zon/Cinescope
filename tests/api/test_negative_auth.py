import allure
from api.api_manager import ApiManager
from constants import WRONG_PASSWORD, BAD_EMAIL


@allure.epic("Auth API")
@allure.feature("Негативные сценарии авторизации")
class TestNegativeApi:

    @allure.story("Неверные данные")
    @allure.title("Логин с неправильным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_bad_password(self, api_manager: ApiManager, create_test_user):
        """
        Попытка логина с неправильным паролем.
        Ожидаем статус 401 и сообщение об ошибке.
        """
        data = {
            "email": create_test_user["email"],
            "password": WRONG_PASSWORD
        }

        with allure.step("Отправляем запрос с неправильным паролем"):
            response = api_manager.auth_api.login_user(data, expected_status=401)

        with allure.step("Проверяем статус и сообщение об ошибке"):
            assert response.status_code == 401, "Статус должен быть 401 при неправильном пароле"
            message = response.json().get("message")
            assert message == "Неверный логин или пароль", f"Неправильное сообщение ошибки: {message}"

    @allure.story("Неверные данные")
    @allure.title("Логин с неправильным email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_bad_email(self, api_manager: ApiManager, create_test_user):
        """
        Попытка логина с неправильным email.
        Ожидаем статус 401 и сообщение об ошибке.
        """
        data = {
            "email": BAD_EMAIL,
            "password": create_test_user["password"]
        }

        with allure.step("Отправляем запрос с неправильным email"):
            response = api_manager.auth_api.login_user(data, expected_status=401)

        with allure.step("Проверяем статус и сообщение об ошибке"):
            assert response.status_code == 401, "Статус должен быть 401 при неправильном email"
            message = response.json().get("message")
            assert message == "Неверный логин или пароль", f"Неправильное сообщение ошибки: {message}"

    @allure.story("Неверные данные")
    @allure.title("Логин с пустым JSON")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_json(self, api_manager: ApiManager):
        """
        Попытка логина с пустым JSON.
        Ожидаем статус 401 и сообщение об ошибке.
        """
        data = {}

        with allure.step("Отправляем пустой JSON"):
            response = api_manager.auth_api.login_user(data, expected_status=401)

        with allure.step("Проверяем статус и сообщение об ошибке"):
            assert response.status_code == 401, "Статус должен быть 401 при пустом JSON"
            message = response.json().get("message")
            assert message == "Неверный логин или пароль", f"Неправильное сообщение ошибки: {message}"
