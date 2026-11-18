from src.core.exception.base import AppError

class UserNotFound(AppError):
    status_code = 404

    def __init__(self, user_id: int | None = None):
        self.user_id = user_id

        super().__init__(f"Пользователь с ID {self.user_id} не найден")


class UserAlreadyExists(AppError):
    status_code = 409

    def __init__(self, email: str):
        self.email = email

        super().__init__(f"Пользователь с таким емейл - {self.email} уже зарегистрирован!")


class UserInvalidCredentials(AppError):
    status_code = 401

    def __init__(self):
        super().__init__("Неверный email или пароль")


class UserInactive(AppError):
    status_code = 403

    def __init__(self):
        super().__init__("Аккаунт пользователя деактивирован")
