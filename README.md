# Cinescope

Фреймворк для автоматизированного тестирования API кино-сервиса (movies, users, auth и т.д.) на Python + pytest.

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)](https://pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure-report-orange)](https://allurereport.org/)  <!-- добавь ссылку на deployed report -->
[![Code Coverage](https://img.shields.io/codecov/c/gh/a1zon/Cinescope)](https://codecov.io/gh/a1zon/Cinescope)  <!-- подключи codecov -->

## О проекте
Cinescope — это демонстрационный проект, показывающий современные практики автотестов API:
- REST API testing с использованием кастомного клиента (requests или httpx)
- Валидация ответов через Pydantic модели
- Проверки состояния в БД после операций (db_requester)
- Ролевая модель авторизации (admin/user/guest)
- Negative/edge cases + parametrized тесты
- Allure reporting для красивых отчётов
- Моки для внешних зависимостей


## Стек
- Python 3.10+
- pytest + pytest-allure
- requests / httpx
- Pydantic (модели)
- SQLAlchemy / psycopg2 (для БД checks)
- Allure-pytest

## Установка и запуск
```bash
git clone https://github.com/a1zon/Cinescope.git
cd Cinescope
pip install -r requirements.txt
# или poetry install, если перейдёшь на poetry