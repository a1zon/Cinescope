BASE_URL =  "https://auth.dev-cinescope.coconutqa.ru"
API_BASE_URL = "https://api.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
MIN_PARAMS = {
            "pageSize": 5,
            "page": 1,
            "published": True,
            "minPrice": 1,
            "maxPrice": 10000
        }
LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
WRONG_PASSWORD = "123123"
BAD_EMAIL = ")*@gmail.cpm"
MOVIES_ENDPOINT = "/movies"

UPDATE_DATA = {

            "price": 999,
            "published": False
        }