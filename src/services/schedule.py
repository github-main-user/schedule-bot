import logging
from datetime import datetime
from typing import Any

import requests

from src.config import settings
from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository

logger = logging.getLogger(__name__)


def fetch_schedule() -> list[dict[str, Any]]:
    """
    Fetches remote schedule, url of which is specified in settings.
    Returns a list of lectures (which are dictionaries).
    In case of an error returns an empty list.
    """
    logger.info("Requesting remote schedule from %s", settings.SCHEDULE_URL)

    raw_lectures = []
    try:
        r = requests.get(url=settings.SCHEDULE_URL, timeout=5)
        r.raise_for_status()

        parsed_result = r.json().get("scheduleChanges", [])
        if isinstance(parsed_result, list):
            raw_lectures = parsed_result
    except requests.exceptions.RequestException as e:
        logging.error("Error during request: %s", e)
    finally:
        logger.info("Fetched %d lectures", len(raw_lectures))
        return raw_lectures


async def update_schedule():
    """Fetches the remote schedule and appends it to local database."""
    logger.info("Starting schedule update")

    session = await get_session()
    repo = ScheduleRepository(session)

    raw_lectures = fetch_schedule()

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
        ).replace(tzinfo=settings.TIMEZONE)

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
