from pydantic import BaseModel, Field, model_validator


class RoomsCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Название комнаты")
    description: str | None = Field(None, max_length=300, description="Описание комнаты")
    price: int = Field(..., gt=0, description="Цена комнаты")
    quantity: int = Field(..., ge=0, description="Количество комнат")


class RoomsResponse(BaseModel):
    id: int
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int


class RoomsPut(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Название комнаты")
    description: str | None = Field(None, max_length=300, description="Описание комнаты")
    price: int = Field(..., gt=0, description="Цена комнаты")
    quantity: int = Field(..., ge=0, description="Количество комнат")


class RoomsPatch(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100, description="Название комнаты")
    description: str | None = Field(None, max_length=300, description="Описание комнаты")
    price: int | None = Field(None, gt=0, description="Цена комнаты")
    quantity: int | None = Field(None, ge=0, description="Количество комнат")

    @model_validator(mode="after")
    def check_not_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None and field != "description":
                raise ValueError(f"{field} cannot be null")
        return self