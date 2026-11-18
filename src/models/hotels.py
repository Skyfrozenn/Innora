from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

class HotelsOrm(Base):
    __tablename__ = "hotels"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(100), unique=True)
    location: Mapped[str] = mapped_column(String(150))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    