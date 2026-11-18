from src.core.exception.base import AppError

class PermissionDeniedException(AppError):
    status_code = 403

    def __init__(self):
        super().__init__(
            detail="У вас нет прав на эту операцию"
        )
