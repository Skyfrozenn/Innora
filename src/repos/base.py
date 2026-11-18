from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base


class BaseRepository:
    model: type[Base]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, **filter_data) -> list[Base]:
        query = select(self.model)
        if filter_data:
            query = query.filter_by(**filter_data)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_one_or_none(self, **filter_data) -> Base | None:
        query = select(self.model).filter_by(**filter_data)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    def add(self, payload_data: dict[str, Any]) -> Base:
        new_obj = self.model(**payload_data)
        self.session.add(new_obj)
        return new_obj
