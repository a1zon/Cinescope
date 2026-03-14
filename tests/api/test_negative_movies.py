import pytest
import allure


@allure.epic("Movies API")
@allure.feature("Негативные сценарии")
class TestMoviesNegative:

    @allure.story("Создание фильма")
    @allure.title("Создание фильма с дублирующим названием")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_duplicate_name(self, super_admin, created_movie, create_test_movie, db_helper):
        """
        Негативный тест: попытка создать фильм с уже существующим названием
        Использует super_admin для создания дубликата
        """
        with allure.step("Проверяем, что фильм существует в БД"):
            movie_in_db = db_helper.get_movie_by_id(created_movie)
            assert movie_in_db is not None, "Фильм должен существовать в БД перед тестом дубликата"

        with allure.step("Пытаемся создать дубликат"):
            duplicate_response = super_admin.api.movies_api.create_movie(create_test_movie, expected_status=409)
            assert duplicate_response.status_code == 409

    @allure.story("Получение фильма")
    @allure.title("Получение несуществующего фильма — 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_movie(self, super_admin):
        """
        Негативный тест: получение несуществующего фильма
        """
        with allure.step("Запрашиваем фильм с несуществующим ID"):
            response = super_admin.api.movies_api.get_single_movie(999999, expected_status=404)
            assert response.status_code == 404

    @allure.story("Удаление фильма")
    @allure.title("Удаление несуществующего фильма — 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_nonexistent_movie(self, super_admin):
        """
        Негативный тест: удаление несуществующего фильма (404)
        """
        with allure.step("Пытаемся удалить несуществующий фильм"):
            response = super_admin.api.movies_api.delete_movie(999999, expected_status=404)
            assert response.status_code == 404

    @allure.story("Ролевая модель")
    @allure.title("Обычный пользователь не может создать фильм")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_common_user_create_movie(self, common_user, create_test_movie):
        """
        Негативный тест: обычный пользователь не может создать фильм
        """
        with allure.step("Пытаемся создать фильм от лица обычного пользователя"):
            response = common_user.api.movies_api.create_movie(create_test_movie, expected_status=403)
            assert response.status_code == 403

    @allure.story("Ролевая модель")
    @allure.title("Удаление фильма — проверка ролевой модели")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.slow
    @pytest.mark.parametrize(
        "deleter_fixture, expected_status",
        [("super_admin", 200), ("common_user", 403)]
    )
    def test_delete_movie_parametrized(self, request, deleter_fixture, expected_status, common_user, created_movie,
                                       db_helper):
        """
        Параметризованный тест на удаление фильма с проверкой ролевой модели
        """
        deleter = request.getfixturevalue(deleter_fixture)
        movie_id = created_movie

        with allure.step(f"Пытаемся удалить фильм от лица {deleter_fixture}"):
            response = deleter.api.movies_api.delete_movie(movie_id=movie_id, expected_status=expected_status)
            assert response.status_code == expected_status

        if expected_status == 200:
            with allure.step("Проверяем, что фильм удалён"):
                response_get = common_user.api.movies_api.get_single_movie(movie_id=movie_id, expected_status=404)
                assert response_get.status_code == 404

                movie_in_db = db_helper.get_movie_by_id(movie_id)
                assert movie_in_db is None, "Фильм всё ещё присутствует в БД после удаления super_admin"
