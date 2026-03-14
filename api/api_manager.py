from clients.auth_api import AuthApi
from clients.genres_api import GenresApi
from clients.movies_api import MoviesApi
from clients.reviews_api import ReviewsApi
from clients.user_api import UserAPI


class ApiManager:
    """
    Центральный менеджер для работы со всеми API-клиентами.
    Каждый экземпляр привязан к одной HTTP-сессии (= одному пользователю).
    """

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthApi(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesApi(session)
        self.genres_api = GenresApi(session)
        self.reviews_api = ReviewsApi(session)

    def close_session(self):
        self.session.close()
