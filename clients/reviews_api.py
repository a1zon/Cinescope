import requests

from constants import API_BASE_URL
from custom_requester.requestor import CustomRequester


class ReviewsApi(CustomRequester):
    """Клиент для работы с API отзывов к фильмам."""

    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_reviews_by_movie(self, movie_id: int, expected_status=200) -> requests.Response:
        """Получение всех отзывов к фильму."""
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}/reviews",
            expected_status=expected_status
        )

    def create_review(self, movie_id: int, review_data: dict, expected_status=200) -> requests.Response:
        """Создание отзыва к фильму (авторизованный пользователь)."""
        return self.send_request(
            method="POST",
            endpoint=f"/movies/{movie_id}/reviews",
            data=review_data,
            expected_status=expected_status
        )

    def update_review(self, movie_id: int, review_data: dict, expected_status=200) -> requests.Response:
        """Обновление отзыва к фильму."""
        return self.send_request(
            method="PUT",
            endpoint=f"/movies/{movie_id}/reviews",
            data=review_data,
            expected_status=expected_status
        )

    def delete_review(self, movie_id: int, expected_status=200) -> requests.Response:
        """Удаление своего отзыва к фильму."""
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}/reviews",
            expected_status=expected_status
        )
