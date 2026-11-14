from fastapi import Depends

from src.service.hotels import HotelService
from src.service.rooms import RoomsService
from src.service.users import UsersService

from src.database.postgres import get_db

from sqlalchemy.ext.asyncio import AsyncSession

def get_hotel_service(session: AsyncSession = Depends(get_db)) -> HotelService:
    return HotelService(session=session)

def get_room_serivce(session: AsyncSession = Depends(get_db)) -> RoomsService:
    return RoomsService(session=session)

def get_user_service(session: AsyncSession = Depends(get_db)) -> UsersService:
    return UsersService(session=session)