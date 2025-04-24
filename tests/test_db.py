import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session


@pytest.mark.asyncio
async def test_get_session() -> None:
    session = await get_session()
    assert isinstance(session, AsyncSession)
    await session.close()
