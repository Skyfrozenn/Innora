from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode="after")
    def check_not_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class HotelsFilters(BaseModel):
    title: str | None = None
    location: str | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=50)
