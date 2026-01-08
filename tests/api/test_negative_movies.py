import pytest


class TestMoviesNegative:

    def test_create_movie_duplicate_name(self, super_admin, created_movie, create_test_movie, db_helper):
        """
        Негативный тест: попытка создать фильм с уже существующим названием
        Использует super_admin для создания дубликата
        """

        movie_in_db = db_helper.get_movie_by_id(created_movie)
        assert movie_in_db is not None, "Фильм должен существовать в БД перед тестом дубликата"

        duplicate_response = super_admin.api.movies_api.create_movie(create_test_movie, expected_status=409)
        assert duplicate_response.status_code == 409

    def test_get_nonexistent_movie(self, super_admin):
        """
        Негативный тест: получение несуществующего фильма
        """
        response = super_admin.api.movies_api.get_single_movie(999999, expected_status=404)
        assert response.status_code == 404

    def test_delete_nonexistent_movie(self, super_admin):
        """
        Негативный тест: удаление несуществующего фильма (404)
        """
        response = super_admin.api.movies_api.delete_movie(999999, expected_status=404)
        assert response.status_code == 404

    def test_common_user_create_movie(self, common_user, create_test_movie):
        """
        Негативный тест: обычный пользователь не может создать фильм
        """
        response = common_user.api.movies_api.create_movie(create_test_movie, expected_status=403)
        assert response.status_code == 403

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

        response = deleter.api.movies_api.delete_movie(movie_id=movie_id, expected_status=expected_status)
        assert response.status_code == expected_status

        # Проверяем, что фильм удалился в БД, если удалял super_admin
        if expected_status == 200:
            response_get = common_user.api.movies_api.get_single_movie(movie_id=movie_id, expected_status=404)
            assert response_get.status_code == 404

            movie_in_db = db_helper.get_movie_by_id(movie_id)
            assert movie_in_db is None, "Фильм всё ещё присутствует в БД после удаления super_admin"
