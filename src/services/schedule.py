from datetime import datetime

from sqlalchemy import insert, select

from src.config import settings
from src.db import get_session
from src.models.schedule import Discipline, Lecture, Teacher
from src.repositories.schedule_repository import ScheduleRepository
from src.utils import schedule_utils


async def update_schedule():
    session = await get_session()

    raw_lectures = schedule_utils.request_raw_schedule()

    for raw_lecture in raw_lectures:

        # teacher

        stmt = select(Teacher).filter_by(
            lastname=raw_lecture["person"]["lastName"],
            firstname=raw_lecture["person"]["name"],
            patronymic=raw_lecture["person"]["secondName"],
        )

        result = await session.execute(stmt)
        teacher = result.scalar_one_or_none()
        if not teacher:
            stmt = (
                insert(Teacher)
                .values(
                    lastname=raw_lecture["person"]["lastName"],
                    firstname=raw_lecture["person"]["name"],
                    patronymic=raw_lecture["person"]["secondName"],
                    birthday=raw_lecture["person"]["birthday"],
                )
                .returning(Teacher)
            )
            result = await session.execute(stmt)
            teacher = result.scalar_one()

        # discipline

        stmt = select(Discipline).filter_by(
            name=raw_lecture["discipline"]["name"],
        )

        result = await session.execute(stmt)
        discipline = result.scalar_one_or_none()

        if not discipline:
            stmt = (
                insert(Discipline)
                .values(
                    name=raw_lecture["discipline"]["name"],
                )
                .returning(Discipline)
            )
            result = await session.execute(stmt)
            discipline = result.scalar_one()

        sCabinet = raw_lecture["svedenCabinet"]
        cabinet = sCabinet["cabinet"] or sCabinet["nameForSchedule"]

        # lecture

        lecture_datetime = datetime.combine(
            date=datetime.fromisoformat(raw_lecture["date"]).date(),
            time=settings.SCHEDULE_TIMES[raw_lecture["lessonId"] - 1],
        )

        stmt = select(Lecture).filter_by(
            date_time=lecture_datetime,
        )

        result = await session.execute(stmt)
        lecture = result.scalar_one_or_none()

        if not lecture:
            stmt = (
                insert(Lecture)
                .values(
                    date_time=lecture_datetime,
                    cabinet=cabinet,
                    is_practice=raw_lecture["eventType"]["name"] != "Лекция",
                    discipline_id=discipline.id,
                    teacher_id=teacher.id,
                )
                .returning(Lecture)
            )
            result = await session.execute(stmt)
            lecture = result.scalar_one()

    await session.commit()
