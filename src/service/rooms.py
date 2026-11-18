from sqlalchemy.ext.asyncio import AsyncSession

from src.service.base import BaseService

from src.repos.hotels import HotelsRepository
from src.repos.rooms import RoomsRepository

from src.core.exception.rooms import RoomNotFound
from src.core.exception.hotels import HotelNotFound

from src.schemas.rooms import (
    RoomsCreate,
    RoomsPatch,
    RoomsResponse,
    RoomsPut,
)


class RoomsService(BaseService):
    schema = RoomsResponse

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.rooms_repo = RoomsRepository(session=session)
        self.hotels_repo = HotelsRepository(session=session)

    async def get_room_by_id(
        self,
        hotel_id: int,
        room_id: int,
    ) -> RoomsResponse:
        room = await self.rooms_repo.get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )
        if room is None:
            raise RoomNotFound(room_id)

        return self.schema.model_validate(room, from_attributes=True)

    async def add_room(
        self,
        hotel_id: int,
        room_data: RoomsCreate,
    ) -> RoomsResponse:
        hotel = await self.hotels_repo.get_one_or_none(id=hotel_id)
        if hotel is None:
            raise HotelNotFound(hotel_id)

        room_data_dict = room_data.model_dump()
        room_data_dict["hotel_id"] = hotel_id

        room = self.rooms_repo.add(room_data_dict)

        await self.session.commit()

        return self.schema.model_validate(room, from_attributes=True)

    async def get_rooms(self, hotel_id: int) -> list[RoomsResponse]:
        rooms = await self.rooms_repo.get_all(hotel_id=hotel_id)

        hotel = await self.hotels_repo.get_one_or_none(id= hotel_id)
        
        if hotel is None:
            raise HotelNotFound(hotel_id)

        return [
            self.schema.model_validate(room, from_attributes=True) for room in rooms
        ]

    async def put_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomsPut,
    ) -> RoomsResponse:
        room = await self.rooms_repo.get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )
        if room is None:
            raise RoomNotFound(room_id)

        new_room = room_data.model_dump()

        for k, v in new_room.items():
            setattr(room, k, v)

        await self.session.commit()

        return self.schema.model_validate(room, from_attributes=True)

    async def patch_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomsPatch,
    ) -> RoomsResponse:
        room = await self.rooms_repo.get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )
        if room is None:
            raise RoomNotFound(room_id)

        new_room = room_data.model_dump(exclude_unset=True)

        if "title" in new_room:
            room.title = new_room["title"]

        if "description" in new_room:
            room.description = new_room["description"]

        if "price" in new_room:
            room.price = new_room["price"]

        if "quantity" in new_room:
            room.quantity = new_room["quantity"]

        await self.session.commit()

        return self.schema.model_validate(room, from_attributes=True)

    async def delete_room(
        self,
        hotel_id: int,
        room_id: int,
    ) -> None:
        room = await self.rooms_repo.get_one_or_none(
            id=room_id,
            hotel_id=hotel_id,
        )
        if room is None:
            raise RoomNotFound(room_id)

        await self.session.delete(room)
        await self.session.commit()
