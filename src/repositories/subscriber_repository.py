from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.subscribers import Subscriber


class SubscriberRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, chat_id: int) -> None:
        new_subscriber = Subscriber(chat_id=chat_id)
        self.session.add(new_subscriber)
        await self.session.commit()

    async def delete(self, chat_id: int) -> None:
        result = await self.get_by_chat_id(chat_id)
        await self.session.delete(result)
        await self.session.commit()

    async def exists(self, chat_id: int) -> bool:
        return bool(await self.get_by_chat_id(chat_id))

    async def get_by_chat_id(self, chat_id: int) -> Subscriber | None:
        stmt = select(Subscriber).filter_by(chat_id=chat_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Subscriber]:
        stmt = select(Subscriber)
        result = await self.session.execute(stmt)
        return result.scalars().all()
