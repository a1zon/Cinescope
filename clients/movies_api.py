import requests

from constants import API_BASE_URL, MOVIES_ENDPOINT
from custom_requester.requestor import CustomRequester


class MoviesApi(CustomRequester):
    """Клиент для работы с Movies API (CRUD-операции над фильмами)."""

    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def create_movie(self, movie_data: dict, expected_status=200) -> requests.Response:
        """Создание нового фильма (требуется роль ADMIN/SUPER_ADMIN)."""
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id: int, expected_status=200) -> requests.Response:
        """Удаление фильма по ID (требуется роль ADMIN/SUPER_ADMIN)."""
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def get_single_movie(self, movie_id: int, expected_status=200) -> requests.Response:
        """Получение информации о фильме по ID."""
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def get_movies(self, params: dict = None, expected_status=200) -> requests.Response:
        """Получение списка фильмов с фильтрацией и пагинацией."""
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

    def update_movie(self, movie_id: int, update_data: dict, expected_status=200) -> requests.Response:
        """Частичное обновление данных фильма (PATCH)."""
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=update_data,
            expected_status=expected_status
        )
