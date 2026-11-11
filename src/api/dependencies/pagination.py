from typing import Annotated

from fastapi import Depends, Query

from src.schemas.hotels import HotelsFilters


def get_hotel_filters(
    title: str | None = None,
    location: str | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> HotelsFilters:
    return HotelsFilters(
        title=title,
        location=location,
        page=page,
        limit=limit,
    )


HotelsFiltersDep = Annotated[HotelsFilters, Depends(get_hotel_filters)]
