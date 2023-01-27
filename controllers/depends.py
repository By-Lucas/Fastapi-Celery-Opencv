from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from db.database import Session


async def get_db():
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()