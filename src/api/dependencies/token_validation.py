import jwt

from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from fastapi import HTTPException, Request, Depends, Response

from src.api.dependencies.service import get_user_service

from src.core.settings import settings

from src.service.users import UsersService

from src.schemas.users import UsersResponse

 


def delete_auth_cookies(response: Response) -> None:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")


async def get_current_user(
    request: Request,
    users_service: UsersService = Depends(get_user_service)
) -> UsersResponse:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Не удалось проверить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = request.cookies.get("access_token")

    if not access_token:
        raise credentials_exception

    try:
        payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        if payload.get("type") != "access":
            raise credentials_exception

        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Срок действия access-токена истёк",
        )

    except InvalidTokenError:
        raise credentials_exception
    
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise credentials_exception

    user = await users_service.get_user(user_id)

    if not user or not user.is_active:
        raise credentials_exception

    return user


async def validation_refresh_token(
    request: Request,
    response: Response,
    users_service: UsersService = Depends(get_user_service)
) -> UsersResponse:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Не удалось проверить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        if payload.get("type") != "refresh":
            delete_auth_cookies(response)
            raise credentials_exception

        user_id = payload.get("sub")
        if user_id is None:
            delete_auth_cookies(response)
            raise credentials_exception

    except ExpiredSignatureError:
        delete_auth_cookies(response)
        raise HTTPException(
            status_code=401,
            detail="Срок действия refresh-токена истёк",
        )

    except InvalidTokenError:
        delete_auth_cookies(response)
        raise credentials_exception

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        delete_auth_cookies(response)
        raise credentials_exception

    user = await users_service.get_user(user_id)

    if not user or not user.is_active:
        delete_auth_cookies(response)
        raise credentials_exception

    return user
