import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.subscribers import Subscriber

logger = logging.getLogger(__name__)


class SubscriberRepository:
    """Gives access to the subscribers from the database."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, chat_id: int) -> None:
        """Adds a subscriber with given `chat_id` to the table."""
        new_subscriber = Subscriber(chat_id=chat_id)
        self.session.add(new_subscriber)
        await self.session.commit()
        logger.info("Subscriber created with chat_id=%s", chat_id)

    async def delete(self, chat_id: int) -> None:
        """Deletes a subscriber from the table by given `chat_id`."""
        subscriber = await self.get_by_chat_id(chat_id)
        if subscriber is None:
            logger.warning(
                "Tried to delete a non-existing subscriber with chat_id=%s", chat_id
            )
            return
        await self.session.delete(subscriber)
        await self.session.commit()
        logger.info("Subscriber deleted with chat_id=%s", chat_id)

    async def exists(self, chat_id: int) -> bool:
        """Checks if a subscriber with given `chat_id` exists."""
        return bool(await self.get_by_chat_id(chat_id))

    async def get_by_chat_id(self, chat_id: int) -> Subscriber | None:
        """
        Looks if a subscriber with given `chat_id` exists in the table.
        Returns either found subscriber or None.
        """
        stmt = select(Subscriber).filter_by(chat_id=chat_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Subscriber]:
        """Returns a sequence of all existing subscribers."""
        stmt = select(Subscriber)
        result = await self.session.execute(stmt)
        return result.scalars().all()
