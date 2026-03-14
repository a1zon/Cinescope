import pytest
import allure


@allure.epic("Auth API")
@allure.feature("Управление пользователями")
class TestUser:

    @allure.story("Создание пользователя")
    @allure.title("Создание пользователя супер-администратором")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, super_admin, creation_user_data):
        with allure.step("Создаём пользователя через SUPER_ADMIN"):
            response = super_admin.api.user_api.create_user(creation_user_data)
            data = response.json()

        with allure.step("Проверяем данные созданного пользователя"):
            assert data.get('id') and data['id'] != '', "ID должен быть не пустым"
            assert data.get('email') == creation_user_data['email']
            assert data.get('fullName') == creation_user_data['fullName']
            assert data.get('roles', []) == creation_user_data['roles']
            assert data.get('verified') is True

    @allure.story("Получение пользователя")
    @allure.title("Получение пользователя по ID и email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        with allure.step("Создаём пользователя"):
            created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()

        with allure.step("Запрашиваем пользователя по ID и email"):
            response_by_id = super_admin.api.user_api.get_user_info(created_user_response['id']).json()
            response_by_email = super_admin.api.user_api.get_user_info(creation_user_data['email']).json()

        with allure.step("Проверяем, что ответы идентичны"):
            assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
            assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
            assert response_by_id.get('email') == creation_user_data['email']
            assert response_by_id.get('fullName') == creation_user_data['fullName']
            assert response_by_id.get('roles', []) == creation_user_data['roles']
            assert response_by_id.get('verified') is True

    @allure.story("Ролевая модель")
    @allure.title("Обычный пользователь не может получить данные другого пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        with allure.step("Запрашиваем данные пользователя от лица обычного пользователя"):
            common_user.api.user_api.get_user_info(common_user.email, expected_status=403)
