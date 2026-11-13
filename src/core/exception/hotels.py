from src.core.exception.base import AppError

class HotelNotFound(AppError):
    status_code = 404

    def __init__(self, hotel_id: int):
        self.hotel_id = hotel_id

        super().__init__(f"Отель с ID {hotel_id} не найден")


class HotelAlreadyExists(AppError):
    status_code = 409

    def __init__(self, title: str):
        self.title = title

        super().__init__(f"Отель с таким названием - {self.title} уже существует!")
