from  custom_requester.requestor import  CustomRequester
from constants import *
import  requests

class MoviesApi(CustomRequester):

    def __init__(self,session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def create_movie (self, movie_data,expected_status = 200) -> requests.Response:

        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200) -> requests.Response:
        endpoint = f"{MOVIES_ENDPOINT}/{movie_id}"
        return self.send_request(
            method="DELETE",
            endpoint=endpoint,
            data=None,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200) -> requests.Response:
        endpoint = f"{MOVIES_ENDPOINT}/{movie_id}"
        return self.send_request(
            method="GET",
            endpoint=endpoint,
            data=None,
            expected_status=expected_status
        )

    def get_movies(self, params: dict = None, expected_status=200) -> requests.Response:
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

    def update_movie(self, movie_id: int, update_data: dict, expected_status=200) -> requests.Response:
        endpoint = f"{MOVIES_ENDPOINT}/{movie_id}"
        return self.send_request(
            method="PATCH",  # ← попробуй PUT вместо PATCH
            endpoint=endpoint,
            data=update_data,
            expected_status=expected_status
        )
