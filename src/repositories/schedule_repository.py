from datetime import date
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.schedule import Lecture


class ScheduleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_lectures_for_day(self, day: date) -> Sequence[Lecture]:
        stmt = select(Lecture).filter(func.date(Lecture.date_time) == day)
        result = await self.session.execute(stmt)
        return result.scalars().all()
