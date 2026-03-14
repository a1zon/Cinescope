import requests

from constants import API_BASE_URL, GENRES_ENDPOINT
from custom_requester.requestor import CustomRequester


class GenresApi(CustomRequester):
    """Клиент для работы с API жанров."""

    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_genres(self, expected_status=200) -> requests.Response:
        """Получение списка всех жанров."""
        return self.send_request(
            method="GET",
            endpoint=GENRES_ENDPOINT,
            expected_status=expected_status
        )

    def get_genre_by_id(self, genre_id: int, expected_status=200) -> requests.Response:
        """Получение жанра по ID."""
        return self.send_request(
            method="GET",
            endpoint=f"{GENRES_ENDPOINT}/{genre_id}",
            expected_status=expected_status
        )

    def create_genre(self, genre_data: dict, expected_status=201) -> requests.Response:
        """Создание нового жанра (только SUPER_ADMIN)."""
        return self.send_request(
            method="POST",
            endpoint=GENRES_ENDPOINT,
            data=genre_data,
            expected_status=expected_status
        )

    def delete_genre(self, genre_id: int, expected_status=200) -> requests.Response:
        """Удаление жанра (только SUPER_ADMIN)."""
        return self.send_request(
            method="DELETE",
            endpoint=f"{GENRES_ENDPOINT}/{genre_id}",
            expected_status=expected_status
        )
