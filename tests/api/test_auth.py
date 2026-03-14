import pytest
import allure
from api.api_manager import ApiManager


@allure.epic("Auth API")
@allure.feature("Регистрация и авторизация")
class TestAuthAPI:

    @allure.story("Регистрация")
    @allure.title("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.slow
    def test_register_user(self, api_manager: ApiManager, test_user_auth):
        """
        Тест на регистрацию пользователя
        """
        with allure.step("Отправляем запрос на регистрацию"):
            response = api_manager.auth_api.register_user(test_user_auth)
            response_data = response.json()

        with allure.step("Проверяем ответ"):
            assert response_data["email"] == test_user_auth["email"], "Email не совпадает"
            assert "id" in response_data, "ID пользователя отсутствует в ответе"
            assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
            assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    @allure.story("Авторизация")
    @allure.title("Регистрация и авторизация пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        with allure.step("Авторизуемся зарегистрированным пользователем"):
            response = api_manager.auth_api.login_user(login_data, expected_status=200)
            response_data = response.json()

        with allure.step("Проверяем наличие токена и корректность email"):
            assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
            assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"
