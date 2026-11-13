from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError

from src.service.base import BaseService
from src.repos.hotels import HotelsRepository
from src.core.exception.hotels import HotelNotFound, HotelAlreadyExists
from src.schemas.hotels import (
    HotelsCreate,
    HotelsPatch,
    HotelsResponse,
    HotelsFilters,
    HotelsPut,
)


class HotelService(BaseService):
    schema = HotelsResponse

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.hotels_repo = HotelsRepository(session=session)

    async def get_hotel_by_id(self, hotel_id: int) -> HotelsResponse:
        hotel = await self.hotels_repo.get_one_or_none(id=hotel_id)
        if hotel is None:
            raise HotelNotFound(hotel_id)
        return self.schema.model_validate(hotel, from_attributes=True)

    async def add_hotel(self, hotel_data: HotelsCreate) -> HotelsResponse:
        hotel = self.hotels_repo.add(hotel_data.model_dump())
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HotelAlreadyExists(hotel_data.title)
        return self.schema.model_validate(hotel, from_attributes=True)

    async def get_hotels(self, hotels_filter: HotelsFilters) -> list[HotelsResponse]:
        hotels = await self.hotels_repo.get_all(hotels_filter.model_dump())
        return [
            self.schema.model_validate(hotel, from_attributes=True) for hotel in hotels
        ]

    async def put_hotel(
        self,
        hotel_id: int,
        hotel_data: HotelsPut,
    ) -> HotelsResponse:
        hotel = await self.hotels_repo.get_one_or_none(id=hotel_id)
        if hotel is None:
            raise HotelNotFound(hotel_id)

        new_hotel = hotel_data.model_dump()
        for k, v in new_hotel.items():
            setattr(hotel, k, v)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HotelAlreadyExists(hotel_data.title)
        return self.schema.model_validate(hotel, from_attributes=True)

    async def patch_hotel(
        self,
        hotel_id: int,
        hotel_data: HotelsPatch,
    ) -> HotelsResponse:
        hotel = await self.hotels_repo.get_one_or_none(id=hotel_id)
        if hotel is None:
            raise HotelNotFound(hotel_id)

        new_hotel = hotel_data.model_dump(exclude_unset=True)

        if title := new_hotel.get("title"):
            hotel.title = title

        if location := new_hotel.get("location"):
            hotel.location = location

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HotelAlreadyExists(hotel_data.title)
        
        return self.schema.model_validate(hotel, from_attributes=True)

    async def delete_hotel(self, hotel_id: int) -> None:
        hotel = await self.hotels_repo.get_one_or_none(id=hotel_id)
        if hotel is None:
            raise HotelNotFound(hotel_id)
        
       
        await self.session.delete(hotel)
        await self.session.commit()
