from fastapi import APIRouter, Body, Depends, status

from src.service.users import UsersService
from src.api.dependencies.service import get_user_service
from src.schemas.users import UserResponse, UserResponseСreate


router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
    description=(
        "Создание нового пользователя. "
        "Email должен быть уникальным."
    ),
)
async def register_user(
    user_data: UserResponseСreate = Body(
        openapi_examples={
            "standard": {
                "summary": "Обычная регистрация",
                "description": "Пример создания нового пользователя.",
                "value": {
                    "name": "Alexander",
                    "email": "alexander@example.com",
                    "password": "StrongPass123!",
                },
            },
            "developer": {
                "summary": "Регистрация разработчика",
                "description": "Пример с другим адресом электронной почты.",
                "value": {
                    "name": "Developer",
                    "email": "developer@example.com",
                    "password": "PythonMaster123@",
                },
            },
            "admin": {
                "summary": "Регистрация администратора",
                "description": "Ещё один пример регистрации.",
                "value": {
                    "name": "Administrator",
                    "email": "admin@example.com",
                    "password": "SecureAdmin123#",
                },
            },
        }
    ),
    users_service: UsersService = Depends(get_user_service),
) -> UserResponse:
    return await users_service.add_user(user_data)
