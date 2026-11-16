from sqlalchemy import select, desc

from src.repos.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):

    model = HotelsOrm

    async def get_all(self, hotels_pagination: dict) -> list[HotelsOrm]:
        limit: int = hotels_pagination.get("limit")
        page: int = hotels_pagination.get("page")

        query = select(HotelsOrm)

        if title := hotels_pagination.get("title"):
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))

        if location := hotels_pagination.get("location"):
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))

        query = (
            query
            .order_by(desc("id"))
            .limit(limit)
            .offset((page - 1) * limit)
        )

        result = await self.session.execute(query)
        hotels = result.scalars().all()

        return list(hotels)
