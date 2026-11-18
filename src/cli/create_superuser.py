import asyncio
from getpass import getpass

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.database.postgres import async_session_maker
from src.schemas.users import UsersCreateSuperUser, UsersWithHashedPassword
from src.core.hash import hash_password
from src.core.enums import UsersRole
from src.models.users import UsersOrm


async def main():
    try:
        name = input("Имя: ")
        email = input("Емейл: ")
        password = getpass("Пароль: ")
        password_confirm = getpass("Повторите пароль: ")

        if password != password_confirm:
            print("Пароли не совпадают!")
            return

        user_data = UsersCreateSuperUser(
            name=name,
            email=email,
            password=password,
        )

        user_with_hash = UsersWithHashedPassword(
            name=user_data.name,
            email=user_data.email,
            hash_password=hash_password(user_data.password),
        )

        user = UsersOrm(
            **user_with_hash.model_dump(),
            role=user_data.role,
        )

        async with async_session_maker() as session:
            query = select(UsersOrm).where(UsersOrm.role == UsersRole.SUPERUSER)

            result = await session.execute(query)
            existing_superuser = result.scalar_one_or_none()

            if existing_superuser is not None:
                print("Суперпользователь уже существует!")
                return

            session.add(user)
            await session.commit()
            await session.refresh(user)

        print(f"Суперпользователь успешно создан: {user.name}")

    except ValidationError as error:
        print(f"Ошибка валидации: {error}")

    except IntegrityError:
        print("Пользователь с таким email уже существует!")

    except SQLAlchemyError as error:
        print(f"Ошибка базы данных: {error}")

    except Exception as error:
        print(f"Непредвиденная ошибка: {error}")


if __name__ == "__main__":
    asyncio.run(main())
