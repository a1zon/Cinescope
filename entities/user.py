from api.api_manager import ApiManager


class User:
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self):
        """
        :param self:
        :return: возвращает кортеж данных пользователя
        """
        creds = {
            "email": self.email,
            "password": self.password
        }
        return creds
