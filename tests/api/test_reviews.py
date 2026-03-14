import pytest
import allure

from utils.data_generator import DataGenerator


@allure.epic("Movies API")
@allure.feature("Отзывы")
class TestReviewsEndpoint:
    """
    Тесты для эндпоинтов /movies/{id}/reviews.
    Покрываем: создание отзыва, получение отзывов, удаление, ролевую модель.
    """

    @allure.story("Получение отзывов")
    @allure.title("Получение отзывов к существующему фильму")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_reviews_for_movie(self, common_user, created_movie):
        """Проверяем, что можно получить список отзывов к фильму."""
        with allure.step("Запрашиваем отзывы к фильму"):
            response = common_user.api.reviews_api.get_reviews_by_movie(
                movie_id=created_movie,
                expected_status=200
            )
            data = response.json()

        with allure.step("Проверяем, что ответ — список"):
            assert isinstance(data, list), "Ответ должен быть списком отзывов"

    @allure.story("Создание отзыва")
    @allure.title("Авторизованный пользователь оставляет отзыв к фильму")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_review(self, common_user, created_movie):
        """Обычный пользователь должен иметь возможность оставить отзыв."""
        review_data = {
            "text": DataGenerator.generate_random_sentence(),
            "rating": 4
        }

        with allure.step("Создаём отзыв"):
            response = common_user.api.reviews_api.create_review(
                movie_id=created_movie,
                review_data=review_data,
                expected_status=201
            )
            data = response.json()

        with allure.step("Проверяем структуру ответа"):
            assert "userId" in data, "Отзыв должен содержать userId"
            assert data["text"] == review_data["text"]
            assert data["rating"] == review_data["rating"]

    @allure.story("Создание отзыва")
    @allure.title("Создание отзыва с невалидным rating")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.xfail(reason="API не валидирует диапазон rating (баг)")
    @pytest.mark.parametrize("rating", [0, -1, 6, 100])
    def test_create_review_invalid_rating(self, common_user, created_movie, rating):
        """Отзыв с rating вне допустимого диапазона должен быть отклонён."""
        review_data = {
            "text": "Тестовый отзыв",
            "rating": rating
        }

        with allure.step(f"Создаём отзыв с rating={rating}"):
            response = common_user.api.reviews_api.create_review(
                movie_id=created_movie,
                review_data=review_data,
                expected_status=400
            )
            assert response.status_code == 400

    @allure.story("Получение отзывов")
    @allure.title("Отзывы к несуществующему фильму — 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_reviews_nonexistent_movie(self, common_user):
        """Запрос отзывов к несуществующему фильму должен вернуть 404."""
        with allure.step("Запрашиваем отзывы к несуществующему фильму"):
            response = common_user.api.reviews_api.get_reviews_by_movie(
                movie_id=999999,
                expected_status=404
            )
            assert response.status_code == 404

    @allure.story("Жизненный цикл отзыва")
    @allure.title("Полный цикл: создание → чтение → удаление отзыва")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_review_lifecycle(self, super_admin, created_movie):
        """
        E2E-тест жизненного цикла отзыва:
        1. Создаём отзыв под SUPER_ADMIN
        2. Проверяем, что он появился в списке отзывов
        3. Удаляем отзыв
        4. Проверяем, что отзыв больше не в списке
        """
        review_text = DataGenerator.generate_random_sentence()

        with allure.step("Создаём отзыв"):
            create_response = super_admin.api.reviews_api.create_review(
                movie_id=created_movie,
                review_data={"text": review_text, "rating": 5},
                expected_status=201
            )
            data = create_response.json()
            assert data["text"] == review_text

        with allure.step("Проверяем, что отзыв присутствует в списке"):
            reviews = super_admin.api.reviews_api.get_reviews_by_movie(
                movie_id=created_movie
            ).json()
            review_texts = [r["text"] for r in reviews]
            assert review_text in review_texts, "Созданный отзыв должен быть в списке"

        with allure.step("Удаляем отзыв"):
            super_admin.api.reviews_api.delete_review(
                movie_id=created_movie,
                expected_status=200
            )

        with allure.step("Проверяем, что отзыв больше не в списке"):
            reviews_after = super_admin.api.reviews_api.get_reviews_by_movie(
                movie_id=created_movie
            ).json()
            review_texts_after = [r["text"] for r in reviews_after]
            assert review_text not in review_texts_after, "Удалённый отзыв не должен быть в списке"
