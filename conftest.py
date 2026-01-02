import  requests
from constants import REGISTER_ENDPOINT, BASE_URL, Roles
import pytest
from utils.data_generator import DataGenerator
from custom_requester.requestor import CustomRequester
from api.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds,AdminCreds
from entities.user import User
from test_pydantic import  TestUser, RegisterUserRequest
from sqlalchemy.orm import Session
from db_requester.bd_client import get_db_session
from typing import Generator
from db_requester.helper import DBHelper


@pytest.fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()



@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

# пусть полежит - вдруг все обратно поломаю
# @pytest.fixture(scope = "function")
# def test_user():
#     """
#     Фикстура для создания тестового юзера
#     """
#     random_email = DataGenerator.generate_random_email()
#     random_name = DataGenerator.generate_random_name()
#     random_password = DataGenerator.generate_random_password()
#
#     return {
#         "email": random_email,
#         "fullName": random_name,
#         "password": random_password,
#         "passwordRepeat": random_password,
#         "roles": ["USER"]
#     }

@pytest.fixture
def create_test_user() -> dict:
    random_password = DataGenerator.generate_random_password()

    user = TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

    return user.model_dump(mode="json")


@pytest.fixture
def test_user_auth() -> dict:
    password = DataGenerator.generate_random_password()

    user = RegisterUserRequest(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=password,
        passwordRepeat=password
    )

    return user.model_dump(mode="json")


@pytest.fixture(scope="function")
def create_test_movie():
    """
    Фикстура для создания тестового фильма
    """
    random_movie = DataGenerator.generate_random_movie_name()
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
def registered_user(requester, test_user_auth):
    """
    Фикстура для регистрации
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user_auth,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user_auth.copy()# нужно потому что в ответе не содержится пароля - а он нужен для атворизации
    assert response_data["email"] == test_user_auth["email"], "Email не совпадает"
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
def auth_user(api_manager, create_test_user):
    """
    Фикстура для авторизации обыным юзером
    """
    api_manager.auth_api.authenticate(create_test_user)
    return api_manager

@pytest.fixture(scope = "session")
def auth_admin(api_manager):
    """
    Фикстура для авторизации админом
    """
    api_manager.auth_api.authenticate_admin()
    return api_manager


@pytest.fixture(scope="function")
def created_movie(auth_admin, create_test_movie):
    """
    Фикстура для создания фильма
    """
    response = auth_admin.movies_api.create_movie(create_test_movie, expected_status=201)
    movie_id = response.json()["id"]

    # Проверяем, что фильм существует
    get_response = auth_admin.movies_api.get_single_movie(movie_id, expected_status=200)
    assert get_response.status_code == 200

    return movie_id

@pytest.fixture
def user_session():
    user_pool =[]

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        email =SuperAdminCreds.USERNAME,
        password = SuperAdminCreds.PASSWORD,
        roles= list(Roles.SUPER_ADMIN.value),
        api= new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(create_test_user):
    updated_data = create_test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return  updated_data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session,super_admin,creation_user_data):
    new_session = user_session()

    admin_user = User(
        AdminCreds.USERNAME,
        AdminCreds.PASSWORD,
        list(Roles.ADMIN.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user