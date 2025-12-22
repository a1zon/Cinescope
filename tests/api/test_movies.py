from conftest import auth_admin
from constants import *

class TestMoviesEndpoint:
    def test_create_movie(self,auth_admin,test_movie):

        """Тест на создание фильма"""

        response = auth_admin.movies_api.create_movie(movie_data=test_movie,expected_status=201)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == test_movie["name"]
        assert data["price"] == test_movie["price"]
        assert data["published"] is True

    def test_delete_movie(self, auth_admin, created_movie):

        """Тест на удаление фильма"""

        response_delete = auth_admin.movies_api.delete_movie(movie_id=created_movie)
        assert  response_delete.status_code == 200
        response_get = auth_admin.movies_api.get_movie(created_movie, expected_status=404)
        assert response_get.status_code == 404

    def test_get_movies_basic_filters(self, auth_admin):

        """ список фильмов с минимальными фильтрами возвращает ОК и правильную структуру"""

        params = MIN_PARAMS

        response = auth_admin.movies_api.get_movies(params=params, expected_status=200)
        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert "count" in data
        assert data["page"] == 1
        assert data["pageSize"] == 5





    """ПАМАГИТИ! я не могу понять почему падают тесты ниже на апдейт фильма с ошибкой 404"""

    def test_update_movie_basic(self, auth_admin, created_movie):

        """"вот пример теста на апдейт"""
        update_data = UPDATE_DATA #обновленная дата фильма

        #вот запрос который сам по себе составлен корректно и не отдает интернал ошибок
        response = auth_admin.movies_api.update_movie(movie_id= created_movie , update_data= update_data, expected_status=200)
        # но почему то еще вот здесь он падает не находя созданный фильм

        updated = response.json()

        assert updated["name"] == update_data["name"]
        assert updated["price"] == update_data["price"]
        assert updated["published"] is False

    def test_update_movie_why_is_it_working(self,auth_admin,test_movie):

        """ Тут думал что проблема в фикстуре создания вильма выше - но нет
        даже создавая его вручную и убеждаясь в успехе этой операции мы не можем его запатчить т к 404"""

        response = auth_admin.movies_api.create_movie(movie_data=test_movie,expected_status=201)
        id = response.json().get("id")
        assert id is not None
        assert response.status_code == 201
        # data = response.json()
        update_data = UPDATE_DATA

        patch_responce = auth_admin.movies_api.update_movie(movie_id= id , update_data= update_data, expected_status=200)
        assert patch_responce.status_code == 200
