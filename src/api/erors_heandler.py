from fastapi import Request
from fastapi.responses import JSONResponse
from src.core.exception.base import AppError


# Обычная функция-обработчик
async def app_exception_handler(request: Request, exc: AppError):
    """
    request - запрос данные
    exc - моя кастомная ошибка
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "detail": exc.detail},
    )