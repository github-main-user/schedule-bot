from datetime import date, datetime
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.schedule import Lecture


class ScheduleRepository:
    """Gives access to the data in Lecture, Teacher, and Discipline tables in database."""

    LECTURE_PRELOAD_OPTIONS = (
        selectinload(Lecture.discipline),
        selectinload(Lecture.teacher),
    )

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_lectures_for_day(self, day: date) -> Sequence[Lecture]:
        """Returns a sequence of lectures for a given day."""
        stmt = (
            select(Lecture)
            .options(*self.LECTURE_PRELOAD_OPTIONS)
            .filter(func.date(Lecture.date_time) == day)
            .order_by(Lecture.date_time)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_next_lecture_after(self, dt: datetime) -> Lecture | None:
        """
        Fetches the nearest lecture after given datetime.
        Returns either that lecture or None.
        """
        stmt = (
            select(Lecture)
            .options(*self.LECTURE_PRELOAD_OPTIONS)
            .filter(Lecture.date_time > dt)
            .order_by(Lecture.date_time)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_lecture_by_datetime(self, dt: datetime) -> Lecture | None:
        """
        Fetches a lecture with exact datetime which was given.
        Returns either that lecture or None.
        """
        stmt = select(Lecture).options(*self.LECTURE_PRELOAD_OPTIONS).filter(Lecture.date_time == dt)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
