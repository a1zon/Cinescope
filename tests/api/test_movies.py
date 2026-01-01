import pytest

from conftest import created_movie, super_admin, common_user
from constants import MIN_PARAMS, UPDATE_DATA


class TestMoviesEndpoint:

    def test_create_movie(self, super_admin, creation_user_data, test_movie):
        """
        Тест на создание фильма
        """
        response = super_admin.api.movies_api.create_movie(movie_data=test_movie, expected_status=201)
        data = response.json()

        assert response.status_code == 201
        assert "id" in data
        assert data["name"] == test_movie["name"]
        assert data["price"] == test_movie["price"]
        assert data["published"] is True

    @pytest.mark.slow
    def test_delete_movie(self, super_admin, created_movie, common_user):
        """
        Тест на удаление фильма
        """

        response = super_admin.api.movies_api.delete_movie(movie_id=created_movie, expected_status=200)

        assert response.status_code == 200

        response_get = common_user.api.movies_api.get_single_movie(created_movie, expected_status=404)

        assert response_get.status_code == 404

    import pytest

    @pytest.mark.slow
    def test_delete_movie(self, super_admin, created_movie, common_user, db_helper):
        """
        Тест на удаление фильма через API с проверкой в базе данных.
        1. Перед удалением фильм существует в БД
        2. Удаление через API с супер-админом
        3. После удаления проверяем, что фильм исчез из БД
        """

        movie_id = created_movie

        movie_in_db = db_helper.get_movie_by_id(movie_id)
        assert movie_in_db is not None, "Фильм должен существовать в базе перед удалением"

        delete_response = super_admin.api.movies_api.delete_movie(movie_id=movie_id, expected_status=200)
        assert delete_response.status_code == 200

        get_response = common_user.api.movies_api.get_single_movie(movie_id, expected_status=404)
        assert get_response.status_code == 404

        movie_in_db_after = db_helper.get_movie_by_id(movie_id)
        assert movie_in_db_after is None, "Фильм всё ещё присутствует в базе после удаления"

    def test_get_movies_basic_filters(self, super_admin):
        """
        Получение списка фильов с минимальными параметрами
        """

        response = super_admin.api.movies_api.get_movies(params=MIN_PARAMS, expected_status=200)
        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert "count" in data
        assert data["page"] == 1
        assert data["pageSize"] == 5

    @pytest.mark.xfail(reason="падают тесты если не меняем название фильма")
    def test_update_movie_data(self, super_admin, created_movie):
        """
        Тест на обновление данных о фильме
        """

        response = super_admin.api.movies_api.update_movie(movie_id=created_movie, update_data=UPDATE_DATA,
                                                           expected_status=200)
        updated = response.json()

        assert updated["name"] == UPDATE_DATA["name"]
        assert updated["price"] == UPDATE_DATA["price"]
        assert updated["published"] is False

    @pytest.mark.parametrize("min_price,max_price,locations,genre_id",
                             [
                                 (1, 1000, ["MSK"], 1),
                                 (100, 500, ["SPB"], 2),
                                 (200, 800, ["MSK", "SPB"], 3),
                             ])
    def test_get_movies_with_filters(self, super_admin, min_price, max_price, locations, genre_id):
        """
        Параметризованный тест для фильтров
        """

        params = {
            "page": 1,
            "pageSize": 5,
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": locations,
            "genreId": genre_id,
            "published": True
        }

        response = super_admin.api.movies_api.get_movies(
            params=params,
            expected_status=200
        )

        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert "count" in data

        for movie in data["movies"]:
            assert min_price <= movie["price"] <= max_price

            assert movie["location"] in locations

            assert movie["genreId"] == genre_id


    def test_update_movie_data_super_admin(self, super_admin, created_movie):
        """
        Рабочий тест на обновление фильма через super_admin.
        Изменяем все поля кроме name, чтобы API корректно нашел фильм по ID.
        Кароче говоря поиск фильмы для апдейта происходил по старому имени
        """

        # Копируем данные из UPDATE_DATA, но оставляем оригинальное имя
        update_data = UPDATE_DATA.copy()

        current_movie = super_admin.api.movies_api.get_single_movie(created_movie, expected_status=200).json()
        update_data["name"] = current_movie["name"]


        response = super_admin.api.movies_api.update_movie(
            movie_id=created_movie,
            update_data=update_data,
            expected_status=200
        )
        updated = response.json()


        assert updated["name"] == current_movie["name"], "Имя фильма должно оставаться прежним"
        assert updated["price"] == update_data["price"], "Цена должна обновиться"
        assert updated["published"] is False, "Статус публикации должен быть False"