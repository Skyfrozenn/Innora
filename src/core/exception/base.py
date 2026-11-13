class AppError(Exception):
    """Базовый класс для всех ошибок приложения"""

    status_code: int = 400

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)
