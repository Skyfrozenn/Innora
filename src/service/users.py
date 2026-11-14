from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError

from src.service.base import BaseService

from src.repos.users import UsersRepository

from src.core.exception.users import UserAlreadyExists, UserNotFound

from src.core.hash import hash_password

from src.schemas.users import (
    UserResponse,
    UserResponseСreate,
    UserWithHashedPassword
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
            
        
         
