from datetime import datetime

from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.config import settings
from src.db import get_session
from src.models.schedule import Discipline, Lecture, Teacher
from src.utils import schedule_utils


async def update_schedule():
    """Fetches the remote schedule and appends it to local database."""
    session = await get_session()

    raw_lectures = schedule_utils.request_raw_schedule()

    for raw_lecture in raw_lectures:

        # teacher

        stmt = pg_insert(Teacher).values(
            lastname=raw_lecture["person"]["lastName"],
            firstname=raw_lecture["person"]["name"],
            patronymic=raw_lecture["person"]["secondName"],
            birthday=raw_lecture["person"]["birthday"],
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

        result = await session.execute(stmt)
        teacher = result.scalar_one()

        # discipline

        stmt = pg_insert(Discipline).values(
            name=raw_lecture["discipline"]["name"],
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["name"],
            set_={"name": stmt.excluded.name},
        ).returning(Discipline)

        result = await session.execute(stmt)
        discipline = result.scalar_one()

        # lecture

        sCabinet = raw_lecture["svedenCabinet"]
        cabinet = sCabinet["cabinet"] or sCabinet["nameForSchedule"]

        lecture_datetime = datetime.combine(
            date=datetime.fromisoformat(raw_lecture["date"]).date(),
            time=settings.SCHEDULE_TIMES[raw_lecture["lessonId"] - 1],
        )

        stmt = pg_insert(Lecture).values(
            date_time=lecture_datetime,
            cabinet=cabinet,
            is_practice=raw_lecture["eventType"]["name"] != "Лекция",
            discipline_id=discipline.id,
            teacher_id=teacher.id,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["date_time"],
            set_={
                "cabinet": stmt.excluded.cabinet,
                "is_practice": stmt.excluded.is_practice,
                "discipline_id": stmt.excluded.discipline_id,
                "teacher_id": stmt.excluded.teacher_id,
            },
        )

        await session.execute(stmt)

    await session.commit()
