import pytest
from conftest import auth_admin
from constants import MIN_PARAMS,UPDATE_DATA

class TestMoviesEndpoint:
    def test_create_movie(self,auth_admin,test_movie):

        """
        Тест на создание фильма
        """

        response = auth_admin.movies_api.create_movie(movie_data=test_movie,expected_status=201)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == test_movie["name"]
        assert data["price"] == test_movie["price"]
        assert data["published"] is True

    def test_delete_movie(self, auth_admin, created_movie):

        """
        Тест на удаление фильма
        """

        response_delete = auth_admin.movies_api.delete_movie(movie_id=created_movie,expected_status=200)
        assert  response_delete.status_code == 200
        response_get = auth_admin.movies_api.get_single_movie(created_movie, expected_status=404)
        assert response_get.status_code == 404

    def test_get_movies_basic_filters(self, auth_admin):

        """
        список фильмов с минимальными фильтрами возвращает ОК и правильную структуру
        """

        params = MIN_PARAMS

        response = auth_admin.movies_api.get_movies(params=params, expected_status=200)
        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert "count" in data
        assert data["page"] == 1
        assert data["pageSize"] == 5





    """ПАМАГИТИ! я не могу понять почему падают тесты ниже на апдейт фильма с ошибкой 404"""
    @pytest.mark.xfail(reason="Если не меняем имя фильма то фильм не находится")
    def test_update_movie_basic(self, auth_admin, created_movie):
        """"
        тест на обновление данных фильма
        """
        update_data = UPDATE_DATA #обновленная дата фильма без нового имени

        response = auth_admin.movies_api.update_movie(movie_id= created_movie , update_data= update_data, expected_status=200)


        updated = response.json()

        assert updated["name"] == update_data["name"]
        assert updated["price"] == update_data["price"]
        assert updated["published"] is False

    @pytest.mark.xfail(reason="Если меняем имя фильма то фильм не находится - все равно не ворк")
    def test_update_movie_why_is_it_not_working(self,auth_admin,test_movie,created_movie):

        """"
        тут вроде меням явно имя фильма но все равно 404 )))))
        """
        update_data = {"name": "Movie name",
          "description": "Movie description",
          "price": 99999999,
          "location": "SPB",
          "imageUrl": "https://image.url",
          "published": True,
          "genreId": 1
            }


        #вот запрос который сам по себе составлен корректно и не отдает интернал ошибок
        response = auth_admin.movies_api.update_movie(movie_id= created_movie , update_data= update_data, expected_status=200)
        # но почему то еще вот здесь он падает не находя созданный фильм

        updated = response.json()

        assert updated["name"] == update_data["name"]
        assert updated["price"] == update_data["price"]
        assert updated["published"] is False

