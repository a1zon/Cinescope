from clients.auth_api import AuthApi
from clients.user_api import UserAPI
from clients.movies_api import MoviesApi

class ApiManager:
    """
    Класс для управления API
    """
    def __init__(self, session):

        self.session = session
        self.auth_api = AuthApi(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesApi(session)
