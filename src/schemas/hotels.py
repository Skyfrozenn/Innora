from pydantic import BaseModel, Field


class HotelsCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Название отеля")
    location: str = Field(..., min_length=3, max_length=150, description="Локация отеля")


class HotelsResponse(HotelsCreate):
    id: int


class HotelsPut(HotelsCreate):
    ...


class HotelsPatch(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100, description="Название отеля")
    location: str | None = Field(None, min_length=3, max_length=150, description="Локация отеля")


class HotelsFilters(BaseModel):
    title: str | None = None
    location: str | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=50)
