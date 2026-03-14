import allure
from models.db_models.movies import FilmDBModel


@allure.epic("Movies API")
@allure.feature("Верификация в БД")
class TestMoviesDB:

    @allure.story("Создание фильма")
    @allure.title("Созданный через API фильм существует в БД")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_movie_db(self, super_admin, db_helper, created_movie):
        """
        Созданный через API фильм находится по ID в БД
        """
        with allure.step("Получаем фильм через API"):
            response = super_admin.api.movies_api.get_single_movie(created_movie)
            data = response.json()

        with allure.step("Проверяем наличие фильма в БД"):
            db_data = db_helper.get_movie_by_id(created_movie)

            assert db_data is not None
            assert data["id"] == db_data.id

    @allure.story("Жизненный цикл фильма")
    @allure.title("Полный цикл: создание → проверка в БД → удаление → проверка в БД")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_movie_lifecycle(self, super_admin, db_helper, create_test_movie):
        """
        Жизненный цикл фильма: создание, проверка в БД, удаление, проверка удаления
        """
        with allure.step("Проверяем, что фильма нет в БД до теста"):
            movie_in_db_before = db_helper.db_session.query(FilmDBModel) \
                .filter(FilmDBModel.name == create_test_movie["name"]) \
                .first()
            assert movie_in_db_before is None, "Фильм уже существует в БД до теста"

        with allure.step("Создаём фильм через API"):
            create_response = super_admin.api.movies_api.create_movie(create_test_movie, expected_status=201)
            created_movie_id = create_response.json()["id"]

        with allure.step("Проверяем, что фильм появился в БД"):
            movie_in_db_after_create = db_helper.get_movie_by_id(created_movie_id)
            assert movie_in_db_after_create is not None, "Фильм не найден в БД после создания"
            assert movie_in_db_after_create.name == create_test_movie["name"]
            assert movie_in_db_after_create.price == create_test_movie["price"]

        with allure.step("Удаляем фильм через API"):
            delete_response = super_admin.api.movies_api.delete_movie(movie_id=created_movie_id, expected_status=200)
            assert delete_response.status_code == 200

        with allure.step("Проверяем, что фильма больше нет в БД"):
            movie_in_db_after_delete = db_helper.get_movie_by_id(created_movie_id)
            assert movie_in_db_after_delete is None, "Фильм всё ещё присутствует в БД после удаления"
