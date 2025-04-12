from datetime import date, datetime
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.schedule import Lecture


class ScheduleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_lectures_for_day(self, day: date) -> Sequence[Lecture]:
        stmt = select(Lecture).filter(func.date(Lecture.date_time) == day)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_next_lecture_after(self, dt: datetime) -> Lecture | None:
        stmt = (
            select(Lecture)
            .options(
                selectinload(Lecture.discipline),
                selectinload(Lecture.teacher),
            )
            .filter(Lecture.date_time > dt)
            .order_by(Lecture.date_time)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
