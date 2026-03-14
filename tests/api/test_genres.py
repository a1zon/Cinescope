import pytest
import allure


@allure.epic("Movies API")
@allure.feature("Жанры")
class TestGenresEndpoint:
    """
    Тесты для эндпоинта /genres.
    Покрываем: получение списка, получение по ID, создание, удаление, ролевую модель.
    """

    @allure.story("Получение жанров")
    @allure.title("Получение списка всех жанров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_genres(self, super_admin):
        """Проверяем, что список жанров возвращается корректно."""
        response = super_admin.api.genres_api.get_genres(expected_status=200)
        data = response.json()

        assert isinstance(data, list), "Ответ должен быть списком"
        assert len(data) > 0, "Список жанров не должен быть пустым"

        # Проверяем структуру первого жанра
        first_genre = data[0]
        assert "id" in first_genre, "Жанр должен содержать id"
        assert "name" in first_genre, "Жанр должен содержать name"

    @allure.story("Получение жанров")
    @allure.title("Получение жанра по ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_genre_by_id(self, super_admin):
        """Получаем первый жанр из списка и проверяем его по ID."""
        genres = super_admin.api.genres_api.get_genres().json()
        genre_id = genres[0]["id"]

        response = super_admin.api.genres_api.get_genre_by_id(genre_id, expected_status=200)
        data = response.json()

        assert data["id"] == genre_id
        assert "name" in data

    @allure.story("Получение жанров")
    @allure.title("Получение несуществующего жанра — 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_genre(self, super_admin):
        """Запрос жанра с несуществующим ID должен вернуть 404."""
        response = super_admin.api.genres_api.get_genre_by_id(999999, expected_status=404)
        assert response.status_code == 404

    @allure.story("Ролевая модель")
    @allure.title("Обычный пользователь может читать жанры")
    @allure.severity(allure.severity_level.NORMAL)
    def test_common_user_can_read_genres(self, common_user):
        """Даже обычный пользователь должен иметь доступ к списку жанров."""
        response = common_user.api.genres_api.get_genres(expected_status=200)
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0
