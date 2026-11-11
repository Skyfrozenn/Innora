from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo = True)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as db:
        yield db
 
 