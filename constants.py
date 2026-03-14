from enum import Enum

# Base URLs
BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
API_BASE_URL = "https://api.dev-cinescope.coconutqa.ru"

# Common headers
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Auth endpoints
LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"

# API endpoints
MOVIES_ENDPOINT = "/movies"
GENRES_ENDPOINT = "/genres"
REVIEWS_ENDPOINT = "/reviews"

# Test data
WRONG_PASSWORD = "123123"
BAD_EMAIL = ")*@gmail.cpm"

MIN_PARAMS = {
    "pageSize": 5,
    "page": 1,
    "published": True,
    "minPrice": 1,
    "maxPrice": 10000
}

UPDATE_DATA = {
    "price": 999,
    "published": False
}


class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
