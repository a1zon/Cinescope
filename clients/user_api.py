import requests

from constants import BASE_URL
from custom_requester.requestor import CustomRequester


class UserAPI(CustomRequester):
    """Клиент для работы с User API (управление пользователями)."""

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    def get_user_info(self, user_id: str, expected_status=200) -> requests.Response:
        """Получение информации о пользователе по ID или email."""
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def delete_user(self, user_id: str, expected_status=204) -> requests.Response:
        """Удаление пользователя (требуется роль SUPER_ADMIN)."""
        return self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def create_user(self, user_data: dict, expected_status=201) -> requests.Response:
        """Создание пользователя напрямую (требуется роль SUPER_ADMIN)."""
        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status
        )
