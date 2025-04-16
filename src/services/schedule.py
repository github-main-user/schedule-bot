import logging
from datetime import datetime

from src.config import settings
from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository
from src.utils import schedule_utils

logger = logging.getLogger(__name__)


async def update_schedule():
    """Fetches the remote schedule and appends it to local database."""
    logger.info("Starting schedule update")

    session = await get_session()
    repo = ScheduleRepository(session)

    raw_lectures = schedule_utils.request_raw_schedule()
    logger.info("Fetched %d lectures", len(raw_lectures))

    for raw_lecture in raw_lectures:

        # teacher

        teacher_data = {
            "lastname": raw_lecture["person"]["lastName"],
            "firstname": raw_lecture["person"]["name"],
            "patronymic": raw_lecture["person"]["secondName"],
            "birthday": raw_lecture["person"]["birthday"],
        }
        teacher = await repo.upsert_teacher(teacher_data)

        # discipline

        discipline_data = {"name": raw_lecture["discipline"]["name"]}
        discipline = await repo.upsert_discipline(discipline_data)

        # lecture

        sCabinet = raw_lecture["svedenCabinet"]
        cabinet = sCabinet["cabinet"] or sCabinet["nameForSchedule"]

        lecture_datetime = datetime.combine(
            date=datetime.fromisoformat(raw_lecture["date"]).date(),
            time=settings.SCHEDULE_TIMES[raw_lecture["lessonId"] - 1],
        )

        lecture_data = {
            "date_time": lecture_datetime,
            "cabinet": cabinet,
            "is_practice": raw_lecture["eventType"]["name"] != "Лекция",
            "discipline_id": discipline.id,
            "teacher_id": teacher.id,
        }
        await repo.upsert_lecture(lecture_data)

    await session.commit()
    logger.info("Schedule update completed successfully")
