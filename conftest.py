import  requests
from constants import REGISTER_ENDPOINT, BASE_URL
import pytest
from utils.data_generator import DataGenerator
from custom_requester.requestor import CustomRequester
from api.api_manager import ApiManager

@pytest.fixture(scope = "function")
def test_user():
    """
    Фикстура для создания тестового юзера
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def test_movie():
    """
    Фикстура для создания тестового фмльма
    """
    random_movie = DataGenerator.generate_random_movie()
    random_price = DataGenerator.generate_random_int()
    random_description = DataGenerator.generate_random_sentence()
    return {
        "name": random_movie,
        "imageUrl": "https://example.com/image.png",
        "price": random_price,
        "description": random_description,
        "location": "SPB",
        "published": True,
        "genreId": 1
    }


@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()# нужно потому что в ответе не содержится пароля - а он нужен для атворизации
    assert response_data["email"] == test_user["email"], "Email не совпадает"
    assert "id" in response_data, "ID пользователя отсутствует в ответе"
    assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
    assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope = "session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope = "session")
def api_manager(session):
    """
     создание экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture(scope="function")
def auth_user(api_manager,test_user):
    """
    Фикстура для авторизации обыным юзером
    """
    api_manager.auth_api.authenticate(test_user)
    return api_manager

@pytest.fixture(scope = "session")
def auth_admin(api_manager):
    """
    Фикстура для авторизации админом
    """
    api_manager.auth_api.authenticate_admin()
    return api_manager


@pytest.fixture(scope="function")
def created_movie(auth_admin, test_movie):
    """
    Фикстура для создания фильма
    """
    response = auth_admin.movies_api.create_movie(test_movie, expected_status=201)
    movie_id = response.json()["id"]

    # Проверяем, что фильм существует
    get_response = auth_admin.movies_api.get_single_movie(movie_id, expected_status=200)
    assert get_response.status_code == 200

    return movie_id
