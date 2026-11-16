from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError

from src.service.base import BaseService

from src.repos.users import UsersRepository

from src.core.exception.users import UserAlreadyExists, UserNotFound, UserInvalidCredentials
from src.core.hash import hash_password, verify_password
from src.core.jwt import create_access_token, create_refresh_token

from src.schemas.users import (
    UserResponse,
    UserResponseСreate,
    UserWithHashedPassword,
    UserLogin
)

class UsersService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.users_repo = UsersRepository(session=session)

    async def add_user(self, user_data: UserResponseСreate) -> UserResponse:
        hashed_password = hash_password(user_data.password)
        user_db = UserWithHashedPassword(
            name=user_data.name,
            email=user_data.email,
            hash_password=hashed_password
        )
        new_user = self.users_repo.add(user_db.model_dump())
        try:
            await self.session.commit()
            await self.session.refresh(new_user)
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExists(user_data.email)
        return UserResponse.model_validate(new_user, from_attributes=True)

    async def login_user(self, user_data: UserLogin) -> dict:
        user = await self.users_repo.get_one_or_none(email = user_data.email)
        if user is None:
            raise UserInvalidCredentials()
        is_password_valid = verify_password(user_data.password, user.hash_password)
        if not is_password_valid:
            raise UserInvalidCredentials()
        access_token = create_access_token({"sub": str(user.id), "type": "access"})
        refresh_token = create_refresh_token({"sub": str(user.id), "type": "refresh"})
        user.is_active = True
        await self.session.commit()
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.users_repo.get_one_or_none(id = user_id)
        if user is None:
            raise UserNotFound(user_id)
        return UserResponse.model_validate(user, from_attributes=True)
