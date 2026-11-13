from src.core.exception.base import AppError


class RoomNotFound(AppError):
    status_code = 404

    def __init__(self, room_id: int):
        self.room_id = room_id

        super().__init__(f"Комната с ID {self.room_id} не найдена")
