from conftest import db_helper
from db_models.movies import FilmDBModel


def test_create_movie_db(super_admin, db_helper, created_movie):
    """
    созданный через апи фильм находиться по id в бд
    """
    response = super_admin.api.movies_api.get_single_movie(created_movie)
    data = response.json()

    db_data = db_helper.get_movie_by_id(created_movie)

    assert isinstance(db_data, object)
    assert db_data is not None

    assert data["id"] == db_data.id


def test_movie_lifecycle(super_admin, db_helper, test_movie):
    """
    ЖЦ фильма )
    """

    # В БД ищем фильм по имени
    movie_in_db_before = db_helper.db_session.query(FilmDBModel) \
        .filter(FilmDBModel.name == test_movie["name"]) \
        .first()
    assert movie_in_db_before is None, "Фильм уже существует в БД до теста"

    # создание фильма через API
    create_response = super_admin.api.movies_api.create_movie(test_movie, expected_status=201)
    created_movie_id = create_response.json()["id"]

    # Проверяем, что фильм появился в БД
    movie_in_db_after_create = db_helper.get_movie_by_id(created_movie_id)
    assert movie_in_db_after_create is not None, "Фильм не найден в БД после создания"
    assert movie_in_db_after_create.name == test_movie["name"]
    assert movie_in_db_after_create.price == test_movie["price"]

    # удаление фильма через API
    delete_response = super_admin.api.movies_api.delete_movie(movie_id=created_movie_id, expected_status=200)
    assert delete_response.status_code == 200

    # Проверяем, что фильма больше нет в БД
    movie_in_db_after_delete = db_helper.get_movie_by_id(created_movie_id)
    assert movie_in_db_after_delete is None, "Фильм всё ещё присутствует в БД после удаления"
