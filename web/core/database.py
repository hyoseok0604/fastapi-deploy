from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.settings import settings

engine = create_async_engine(str(settings.postgres_uri))

async_session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DatabaseDependency = Annotated[AsyncSession, Depends(get_db)]
