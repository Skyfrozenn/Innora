import jwt

from jwt.exceptions import InvalidTokenError

from fastapi import HTTPException, Request, Depends

from src.api.dependencies.service import get_user_service

from src.core.settings import settings

from src.service.users import UsersService

from src.schemas.users import UserResponse


async def get_current_user(
    request: Request,
    users_service: UsersService = Depends(get_user_service)
):
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
    except InvalidTokenError:
        raise credentials_exception

    user = await users_service.get_user(int(user_id))

    if not user.is_active:
        raise credentials_exception

    return UserResponse.model_validate(user, from_attributes=True)
    
    

