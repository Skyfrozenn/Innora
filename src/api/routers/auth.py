from fastapi import APIRouter, Body, Depends, Path, status, Response, Request

from src.service.users import UsersService

from src.api.dependencies.service import get_user_service
from src.api.dependencies.token_validation import get_current_user
from src.api.dependencies.permissions import require_superuser

from src.schemas.users import UsersResponse, UsersResponseСreate, UsersLogin


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
    user_data: UsersResponseСreate = Body(
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
                "summary": "Регистрация покупателя",
                "description": "Ещё один пример регистрации.",
                "value": {
                    "name": "Buyeristrator",
                    "email": "buуer@example.com",
                    "password": "buyerAdmin123#",
                },
            },
        }
    ),
    users_service: UsersService = Depends(get_user_service),
) -> UsersResponse:
    return await users_service.add_user(user_data)


@router.post(
    "/login",
    summary="Аутентификация пользователя",
    description="Аутентификация пользователя и генерация токенов"
)
async def login_user(
    response: Response,
    user_data: UsersLogin,
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
async def me(current_user = Depends(get_current_user)) -> UsersResponse:
    return current_user


@router.patch("/{user_id}/assign-admin")
async def assign_admin(
    user_id: int = Path(ge=1, le=2147483647),
    user_service : UsersService = Depends(get_user_service),
    _ = Depends(require_superuser)
) -> UsersResponse:
    return await user_service.assign_admin(user_id)

@router.patch("/{user_id}/revoke-admin")
async def revoke_admin(
    user_id: int = Path(ge=1, le=2147483647),
    user_service : UsersService = Depends(get_user_service),
    _ = Depends(require_superuser)
) -> UsersResponse:
    return await user_service.revoke_admin(user_id)