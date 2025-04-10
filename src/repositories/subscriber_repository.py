from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.subscribers import Subscriber


class SubscriberRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, subscriber: Subscriber) -> None:
        self.session.add(subscriber)
        await self.session.commit()

    async def delete(self, subscriber: Subscriber) -> None:
        await self.session.delete(subscriber)
        await self.session.commit()

    async def get_all(self) -> Sequence[Subscriber]:
        stmt = select(Subscriber)
        result = await self.session.execute(stmt)
        return result.scalars().all()
