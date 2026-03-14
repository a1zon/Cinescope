import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, field_validator

from constants import Roles


class TestUser(BaseModel):
    """Модель тестового пользователя для создания через SUPER_ADMIN."""
    model_config = ConfigDict(use_enum_values=True)

    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(
        ..., min_length=1, max_length=20,
        description="Должен совпадать с полем password"
    )
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class RegisterUserResponse(BaseModel):
    """Модель ответа на регистрацию — валидирует структуру JSON от сервера."""
    id: str
    email: str = Field(
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Email пользователя"
    )
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты. Ожидается ISO 8601.")
        return value


class RegisterUserRequest(BaseModel):
    """Модель запроса на регистрацию пользователя."""
    email: str
    fullName: str
    password: str
    passwordRepeat: str

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value, info):
        if value != info.data.get("password"):
            raise ValueError("Пароли не совпадают")
        return value


class CreateUserRequest(RegisterUserRequest):
    """Расширенный запрос для создания пользователя с указанием ролей и статуса."""
    roles: list[Roles]
    verified: bool
    banned: bool


class MovieResponse(BaseModel):
    """Модель ответа при получении фильма из API."""
    id: int
    name: str
    price: float
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    location: str
    published: bool
    rating: float
    genreId: int
    createdAt: str


class GenreResponse(BaseModel):
    """Модель жанра из API."""
    id: int
    name: str


class ReviewResponse(BaseModel):
    """Модель отзыва из API."""
    userId: str
    text: str
    rating: int
    createdAt: str
