from conftest import auth_admin


class TestMoviesEndpoint:
    def test_create_movie_duplicate_name(self, auth_admin, test_movie):
        """Негативный тест: попытка создать фильм с уже существующим названием """

        first_response = auth_admin.movies_api.create_movie(test_movie, expected_status=201)
        movie_id = first_response.json()["id"]

        duplicate_response = auth_admin.movies_api.create_movie(
            test_movie, expected_status=409
        )
        assert duplicate_response.status_code == 409

    def test_get_nonexistent_movie(self, auth_admin):
        """Негативный тест: получение несуществующего фильма """
        response = auth_admin.movies_api.get_movie(999999, expected_status=404)
        assert response.status_code == 404

    def test_delete_nonexistent_movie(self, auth_admin):
        """Негативный тест: удаление несуществующего фильма (404)"""
        response = auth_admin.movies_api.delete_movie(999999, expected_status=404)
        assert response.status_code == 404
