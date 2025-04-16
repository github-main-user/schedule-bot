import logging
from datetime import date, datetime
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.schedule import Discipline, Lecture, Teacher

logger = logging.getLogger(__name__)


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

    async def upsert_teacher(self, teacher_data: dict) -> Teacher:
        """
        Creates a new teacher or updates an existing record.
        Returns that created/updated object.
        """
        stmt = pg_insert(Teacher).values(
            lastname=teacher_data["lastname"],
            firstname=teacher_data["firstname"],
            patronymic=teacher_data["patronymic"],
            birthday=teacher_data["birthday"],
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["lastname", "firstname", "patronymic"],
            set_={
                "lastname": stmt.excluded.lastname,
                "firstname": stmt.excluded.firstname,
                "patronymic": stmt.excluded.patronymic,
                "birthday": stmt.excluded.birthday,
            },
        ).returning(Teacher)

        result = await self.session.execute(stmt)
        teacher = result.scalar_one()
        logger.info("Upserted teacher: %s (%s)", teacher.initials, teacher.birthday)
        return teacher

    async def upsert_discipline(self, discipline_data: dict) -> Discipline:
        """
        Creates a new discipline or updates an existing record.
        Returns that created/updated object.
        """
        stmt = pg_insert(Discipline).values(name=discipline_data["name"])
        stmt = stmt.on_conflict_do_update(
            index_elements=["name"],
            set_={"name": stmt.excluded.name},
        ).returning(Discipline)

        result = await self.session.execute(stmt)
        discipline = result.scalar_one()
        logger.info("Upserted discipline: %s", discipline.name)
        return discipline

    async def upsert_lecture(self, lecture_data: dict) -> Lecture:
        """
        Creates a new lecture or updates an existing record.
        Returns that created/updated object.
        """
        stmt = pg_insert(Lecture).values(
            date_time=lecture_data["date_time"],
            cabinet=lecture_data["cabinet"],
            is_practice=lecture_data["is_practice"],
            discipline_id=lecture_data["discipline_id"],
            teacher_id=lecture_data["teacher_id"],
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["date_time"],
            set_={
                "cabinet": stmt.excluded.cabinet,
                "is_practice": stmt.excluded.is_practice,
                "discipline_id": stmt.excluded.discipline_id,
                "teacher_id": stmt.excluded.teacher_id,
            },
        ).returning(Lecture)

        result = await self.session.execute(stmt)
        lecture = result.scalar_one()
        logger.info(
            "Upserted lecture at (cabinet: %s, discipline_id: %s, teacher_id: %s)",
            lecture.date_time,
            lecture.cabinet,
            lecture.discipline_id,
            lecture.teacher_id,
        )
        return lecture
