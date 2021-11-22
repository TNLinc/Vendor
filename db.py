from typing import Generator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)
SessionBuilder = sessionmaker(autocommit=False, bind=engine, class_=AsyncSession)


async def create_session() -> Generator:
    try:
        new_session = SessionBuilder()
        yield new_session
    finally:
        await new_session.close()
