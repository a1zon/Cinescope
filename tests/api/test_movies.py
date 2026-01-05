import pytest
import  allure
from conftest import created_movie, super_admin, common_user
from constants import MIN_PARAMS, UPDATE_DATA


@allure.epic("Movies API")
@allure.feature("Управление фильмами")
class TestMoviesEndpoint:

    @allure.story("Создание фильма")
    @allure.title("Создание фильма супер-администратором")
    @allure.description("""
    Проверяем, что супер-администратор может создать фильм.
    Ожидаемый результат:
    - статус 201
    - фильм содержит id
    - данные фильма соответствуют отправленным
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_create_movie(self, super_admin, create_test_movie):

        with allure.step("Отправляем запрос на создание фильма"):
            response = super_admin.api.movies_api.create_movie(
                movie_data=create_test_movie,
                expected_status=201
            )

        with allure.step("Проверяем ответ"):
            data = response.json()

            assert response.status_code == 201
            assert "id" in data
            assert data["name"] == create_test_movie["name"]
            assert data["price"] == create_test_movie["price"]
            assert data["published"] is True


    @allure.story("Удаление фильма")
    @allure.title("Удаление фильма супер-администратором")
    @allure.description("""
    Шаги:
    1. Удаляем фильм через API под супер-админом
    2. Проверяем, что обычный пользователь больше не может получить фильм
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.slow
    def test_delete_movie(self, super_admin, created_movie, common_user):

        with allure.step("Удаляем фильм через API"):
            response = super_admin.api.movies_api.delete_movie(
                movie_id=created_movie,
                expected_status=200
            )
            assert response.status_code == 200

        with allure.step("Проверяем, что фильм недоступен для обычного пользователя"):
            response_get = common_user.api.movies_api.get_single_movie(
                created_movie,
                expected_status=404
            )
            assert response_get.status_code == 404


    @allure.story("Получение списка фильмов")
    @allure.title("Получение списка фильмов с минимальными параметрами")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_basic_filters(self, super_admin):

        with allure.step("Запрашиваем список фильмов"):
            response = super_admin.api.movies_api.get_movies(
                params=MIN_PARAMS,
                expected_status=200
            )

        with allure.step("Проверяем структуру ответа"):
            data = response.json()

            assert "movies" in data
            assert isinstance(data["movies"], list)
            assert "count" in data
            assert data["page"] == 1
            assert data["pageSize"] == 5


    @allure.story("Обновление фильма")
    @allure.title("Обновление данных фильма (известная ошибка)")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.xfail(reason="API некорректно обрабатывает обновление имени фильма")
    def test_update_movie_data(self, super_admin, created_movie):

        with allure.step("Отправляем запрос на обновление фильма"):
            response = super_admin.api.movies_api.update_movie(
                movie_id=created_movie,
                update_data=UPDATE_DATA,
                expected_status=200
            )

        with allure.step("Проверяем обновлённые данные"):
            updated = response.json()

            assert updated["name"] == UPDATE_DATA["name"]
            assert updated["price"] == UPDATE_DATA["price"]
            assert updated["published"] is False


    @allure.story("Фильтрация фильмов")
    @allure.title("Фильтрация фильмов по параметрам")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "min_price,max_price,locations,genre_id",
        [
            (1, 1000, ["MSK"], 1),
            (100, 500, ["SPB"], 2),
            (200, 800, ["MSK", "SPB"], 3),
        ]
    )
    def test_get_movies_with_filters(
        self, super_admin, min_price, max_price, locations, genre_id
    ):

        params = {
            "page": 1,
            "pageSize": 5,
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": locations,
            "genreId": genre_id,
            "published": True
        }

        with allure.step("Запрашиваем список фильмов с фильтрами"):
            response = super_admin.api.movies_api.get_movies(
                params=params,
                expected_status=200
            )

        with allure.step("Проверяем, что фильмы соответствуют фильтрам"):
            data = response.json()

            assert "movies" in data
            assert isinstance(data["movies"], list)

            for movie in data["movies"]:
                assert min_price <= movie["price"] <= max_price
                assert movie["location"] in locations
                assert movie["genreId"] == genre_id


    @allure.story("Обновление фильма")
    @allure.title("Корректное обновление фильма без изменения имени")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_movie_data_super_admin(self, super_admin, created_movie):

        with allure.step("Получаем текущие данные фильма"):
            current_movie = super_admin.api.movies_api.get_single_movie(
                created_movie,
                expected_status=200
            ).json()

        with allure.step("Готовим данные для обновления"):
            update_data = UPDATE_DATA.copy()
            update_data["name"] = current_movie["name"]

        with allure.step("Отправляем запрос на обновление"):
            response = super_admin.api.movies_api.update_movie(
                movie_id=created_movie,
                update_data=update_data,
                expected_status=200
            )

        with allure.step("Проверяем обновлённые данные"):
            updated = response.json()

            assert updated["name"] == current_movie["name"]
            assert updated["price"] == update_data["price"]
            assert updated["published"] is False
