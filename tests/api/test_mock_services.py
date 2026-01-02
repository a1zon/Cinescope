import datetime
from datetime import datetime
from unittest.mock import Mock

import pytz
import requests

from models.pydantic_models import WorldClockResponse, WhatIsTodayResponse


#
class BaseTimeTest:
    """Базовый класс с общими методами для тестов времени"""

    @classmethod
    def get_daytime(cls) -> WorldClockResponse:
        """Получает текущее время от worldclockapi"""
        response = requests.get("http://worldclockapi.com/api/json/utc/now", timeout=10)
        assert response.status_code == 200, "Сервер не отвечает"
        return WorldClockResponse(**response.json())


class TestTodayIsHolidayApi(BaseTimeTest):

    def test_daytime_response(self):
        # Вызываем метод из базового класса
        daytime_response = self.get_daytime()
        current_daytime = daytime_response.currentDateTime

        # Сравниваем с текущим временем
        assert current_daytime == datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Дата не совпадает"

    def test_what_is_today(self):
        # Вызываем тот же метод
        daytime_response = self.get_daytime()

        # Исправляем: используем json= вместо data=
        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            json={"currentDateTime": daytime_response.currentDateTime}  # Упрощённо
        )


class TestMockExactly(BaseTimeTest):

    def test_what_is_today_mock(self, mocker):
        mocker.patch.object(
            BaseTimeTest,  # Класс, где находится метод
            'get_daytime',  # Имя метода
            return_value=Mock(
                currentDateTime="2025-01-01T00:00Z"  # Фиксированная дата
            )
        )

        # Вызываем метод (теперь он замокан)
        world_clock_response = self.get_daytime()  # Вернёт "2025-01-01T00:00Z"

        # Проверяем, что мок сработал
        assert world_clock_response.currentDateTime == "2025-01-01T00:00Z"

        # Отправляем запрос на наш сервис
        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            json={"currentDateTime": world_clock_response.currentDateTime}
        )

        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        assert what_is_today_data.message == "Новый год", "ДОЛЖЕН БЫТЬ НОВЫЙ ГОД!"

    @classmethod
    def setup_wiremock_for_worldclockap(cls):
        """
        Настройка WireMock для эмуляции worldclockapi
        """
        wiremock_url = "http://localhost:8080/__admin/mappings"

        mapping = {
            "request": {
                "method": "GET",
                "url": "/wire/mock/api/json/utc/now"  # Эмулируем запрос к worldclockapi
            },
            "response": {
                "status": 200,
                "body": '''{
                    "$id": "1",
                    "currentDateTime": "2025-03-08T00:00Z",
                    "utcOffset": "00:00",
                    "isDayLightSavingsTime": false,
                    "dayOfTheWeek": "Wednesday",
                    "timeZoneName": "UTC",
                    "currentFileTime": 1324567890123,
                    "ordinalDate": "2025-1",
                    "serviceResponse": null
                }''',
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        }

        response = requests.post(wiremock_url, json=mapping)
        assert response.status_code in [200, 201], f"Не удалось настроить WireMock: {response.status_code}"

    def test_what_is_today_BY_WIREMOCK(self):
        """
        Тест с использованием WireMock
        """
        # Запускаем настройку WireMock
        self.setup_wiremock_for_worldclockap()

        # Выполняем запрос к WireMock (имитация worldclockapi)
        world_clock_response = requests.get(
            "http://localhost:8080/wire/mock/api/json/utc/now",
            timeout=5
        )

        assert world_clock_response.status_code == 200, "WireMock сервис недоступен"

        # Парсим JSON-ответ
        current_date_time = WorldClockResponse(**world_clock_response.json()).currentDateTime

        # Проверяем, что получили нужную дату
        assert current_date_time == "2025-03-08T00:00Z"

        # Выполняем запрос к тестируемому сервису what_is_today
        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            json={"currentDateTime": current_date_time}  # Используем json=
        )

        # Проверяем статус ответа
        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"

        # Парсим ответ
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())

        # Проверяем результат
        assert what_is_today_data.message == "Международный женский день", \
            f"Ожидалось 8 марта, получено: {what_is_today_data.message}"
