from fastapi import APIRouter, Body, Depends, Path

from src.api.dependencies.service import get_hotel_service
from src.api.dependencies.pagination import HotelsFiltersDep
from src.api.dependencies.permissions import require_admin_or_superuser

from src.service.hotels import HotelService

from src.schemas.hotels import HotelsCreate, HotelsPatch, HotelsResponse, HotelsPut


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение отелей",
    description="Получение списка отелей с фильтрацией и пагинацией.",
)
async def get_hotels(
    hotels_pagination: HotelsFiltersDep,
    hotel_service: HotelService = Depends(get_hotel_service)
) -> list[HotelsResponse]:
    return await hotel_service.get_hotels(hotels_pagination)


@router.get(
    "/{hotel_id}",
    summary="Получение отеля",
    description="Получение отеля по ID"
)
async def get_hotel_by_id(
    hotel_id: int = Path(ge=1, le=2147483647),
    hotel_service: HotelService = Depends(get_hotel_service),
) -> HotelsResponse:
    return await hotel_service.get_hotel_by_id(hotel_id)


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Удаление отеля по ID.",
    status_code=204,
)
async def delete_hotel(
    hotel_id: int = Path(ge=1, le=2147483647),
    current_user = Depends(require_admin_or_superuser),
    hotel_service: HotelService = Depends(get_hotel_service),
) -> None:
    await hotel_service.delete_hotel(current_user, hotel_id)


@router.post(
    "",
    summary="Добавление отеля",
    description="Создание отеля с указанием названия и локации.",
    status_code=201,
)
async def new_hotel(
    hotel_data: HotelsCreate = Body(
        openapi_examples={
            "moscow": {
                "summary": "Отель в Москве",
                "description": "Пример создания отеля в столице.",
                "value": {
                    "title": "Гранд Отель",
                    "location": "Москва",
                },
            },
            "petersburg": {
                "summary": "Отель в Санкт-Петербурге",
                "value": {
                    "title": "Северная звезда",
                    "location": "Санкт-Петербург",
                },
            },
            "sochi": {
                "summary": "Отель в Сочи",
                "value": {
                    "title": "Морской бриз",
                    "location": "Сочи",
                },
            },
            "kaliningrad": {
                "summary": "Отель в Калининграде",
                "value": {
                    "title": "Золотой берег",
                    "location": "Калининград",
                },
            },
            "kazan": {
                "summary": "Отель в Казани",
                "value": {
                    "title": "Лесная сказка",
                    "location": "Казань",
                },
            },
        }
    ),
    hotel_service: HotelService = Depends(get_hotel_service),
    current_user = Depends(require_admin_or_superuser)
) -> HotelsResponse:
    return await hotel_service.add_hotel(current_user.id, hotel_data)


@router.put(
    "/{hotel_id}",
    summary="Полное обновление отеля",
    description="Полная замена названия и локации отеля по ID.",
)
async def put_hotel(
    hotel_data: HotelsPut,
    current_user = Depends(require_admin_or_superuser),
    hotel_id: int = Path(ge=1, le=2147483647),
    hotel_service: HotelService = Depends(get_hotel_service)
) -> HotelsResponse:
    return await hotel_service.put_hotel(hotel_id, current_user, hotel_data)
     

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление отеля",
    description="Частичное изменение названия, локации или обоих полей по ID.",
)
async def patch_hotel(
    hotel_data: HotelsPatch,
    current_user = Depends(require_admin_or_superuser),
    hotel_id: int = Path(ge=1, le=2147483647),
    hotel_service: HotelService = Depends(get_hotel_service)
) -> HotelsResponse:
    return await hotel_service.patch_hotel(hotel_id, current_user, hotel_data)
