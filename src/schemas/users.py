from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserResponseСreate(BaseModel):
    name: str = Field(
        ...,
        min_length=4,
        max_length=20,
        description="Имя пользователя от 4 до 20 символов",
    )
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Пароль не менее 8 символов!",
    )

    @field_validator("password")
    @classmethod
    def validation_password(cls, value: str) -> str:
        if not any(item.isupper() for item in value):
            raise ValueError("В пароле должен быть хоть один большой символ!")

        special_characters = "!@#$%^&*()_+/,.?[]"
        if not any(item in special_characters for item in value):
            raise ValueError(
                f"В пароле должен быть хоть один спецсимвол {special_characters}"
            )

        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserWithHashedPassword(BaseModel):
    name: str
    email: EmailStr
    hash_password: str = Field(..., max_length=255)
