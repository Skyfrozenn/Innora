from fastapi import APIRouter, Body, Depends, status, Response, Request

from src.service.users import UsersService

from src.api.dependencies.service import get_user_service
from src.api.dependencies.token_validation import get_current_user

from src.schemas.users import UserResponse, UserResponseСreate, UserLogin


router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"],
)


@router.post(
    "/register",
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


@router.post(
    "/login",
    summary="Аутентификация пользователя",
    description="Аутентификация пользователя и генерация токенов"
)
async def login_user(
    response: Response,
    user_data: UserLogin,
    user_service: UsersService = Depends(get_user_service)
) -> dict:

    tokens = await user_service.login_user(user_data)

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        max_age=30 * 60
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        max_age=7 * 24 * 60 * 60
    )
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/me")
async def me(current_user = Depends(get_current_user)):
    return current_user