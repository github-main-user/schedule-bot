import requests

from src.config import settings
from src.models.schedule import Lecture

from . import messages


def request_raw_schedule() -> list:
    r = requests.get(url=settings.SCHEDULE_URL, timeout=5)
    r.raise_for_status()

    return r.json().get("scheduleChanges", [])


def format_lecture(lecture: Lecture) -> str:
    return messages.LECTURE_BASE_TEMPLATE.format(
        time=lecture.date_time,
        name=lecture.name,
        event_type="Практика" if lecture.is_practice else "Лекция",
        cabinet=lecture.cabinet,
    )


def format_lecture_verbose(lecture: Lecture) -> str:
    return messages.LECTURE_VERBOSE_TEMPLATE.format(
        time=lecture.date_time,
        name=lecture.name,
        event_type="Практика" if lecture.is_practice else "Лекция",
        cabinet=lecture.cabinet,
        teacher=lecture.teacher.fullname,
        age=lecture.teacher.age,
    )
