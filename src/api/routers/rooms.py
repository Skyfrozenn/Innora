from fastapi import APIRouter, Body, Depends, Path

from src.api.dependencies.service import get_room_serivce
from src.service.rooms import RoomsService

from src.schemas.rooms import (
    RoomsCreate,
    RoomsPatch,
    RoomsResponse,
    RoomsPut,
)

router = APIRouter(
    prefix="/hotels/{hotel_id}/rooms",
    tags=["Номера"],
)


@router.get(
    "",
    summary="Получение комнат отеля",
    description="Получение списка всех комнат конкретного отеля.",
)
async def get_rooms(
    hotel_id: int = Path(ge=1, le=2147483647),
    room_service: RoomsService = Depends(get_room_serivce),
) -> list[RoomsResponse]:
    return await room_service.get_rooms(hotel_id)


@router.get(
    "/{room_id}",
    summary="Получение комнаты",
    description="Получение комнаты конкретного отеля по ID.",
)
async def get_room_by_id(
    hotel_id: int = Path(ge=1, le=2147483647),
    room_id: int = Path(ge=1, le=2147483647),
    room_service: RoomsService = Depends(get_room_serivce),
) -> RoomsResponse:
    return await room_service.get_room_by_id(hotel_id, room_id)


@router.delete(
    "/{room_id}",
    summary="Удаление комнаты",
    description="Удаление комнаты конкретного отеля по ID.",
    status_code=204,
)
async def delete_room(
    hotel_id: int = Path(ge=1, le=2147483647),
    room_id: int = Path(ge=1, le=2147483647),
    room_service: RoomsService = Depends(get_room_serivce),
) -> None:
    await room_service.delete_room(hotel_id, room_id)


@router.post(
    "",
    summary="Добавление комнаты",
    description="Создание комнаты в конкретном отеле.",
    status_code=201,
)
async def new_room(
    room_data: RoomsCreate = Body(
        openapi_examples={
            "standard": {
                "summary": "Стандартная комната",
                "value": {
                    "title": "Standard",
                    "description": "Стандартная комната с двуспальной кроватью.",
                    "price": 5000,
                    "quantity": 20,
                },
            },
            "luxury": {
                "summary": "Комната люкс",
                "value": {
                    "title": "Luxury",
                    "description": "Просторная комната повышенной комфортности.",
                    "price": 12000,
                    "quantity": 5,
                },
            },
        }
    ),
    hotel_id: int = Path(ge=1, le=2147483647),
    room_service: RoomsService = Depends(get_room_serivce),
) -> RoomsResponse:
    return await room_service.add_room(hotel_id, room_data)


@router.put(
    "/{room_id}",
    summary="Полное обновление комнаты",
    description="Полная замена данных комнаты конкретного отеля.",
)
async def put_room(
    room_data: RoomsPut,
    hotel_id: int = Path(ge=1, le=2147483647),
    room_id: int = Path(ge=1, le=2147483647),
    room_service: RoomsService = Depends(get_room_serivce),
) -> RoomsResponse:
    return await room_service.put_room(hotel_id, room_id, room_data)


@router.patch(
    "/{room_id}",
    summary="Частичное обновление комнаты",
    description="Частичное изменение данных комнаты конкретного отеля.",
)
async def patch_room(
    room_data: RoomsPatch,
    hotel_id: int = Path(ge=1, le=2147483647),
    room_id: int = Path(ge=1, le=2147483647),
    room_service: RoomsService = Depends(get_room_serivce),
) -> RoomsResponse:
    return await room_service.patch_room(hotel_id, room_id, room_data)
