from src.core.exception.base import AppError

class UserNotFound(AppError):
    status_code = 404

    def __init__(self, user_id: int):
        self.user_id = user_id

        super().__init__(f"Отель с ID {self.user_id} не найден")


class UserAlreadyExists(AppError):
    status_code = 409

    def __init__(self, email: str):
        self.email = email

        super().__init__(f"Пользователь с таким емейл - {self.email} уже зарегистрирован!")
