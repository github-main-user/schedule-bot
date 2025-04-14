import requests

from src.config import settings
from src.models.schedule import Lecture

from . import messages


def request_raw_schedule() -> list:
    """
    Fetches the remote schedule url of which is specified in settings.
    Raises error for status.
    Returns a list of lectures (which are dictionaries).
    """
    r = requests.get(url=settings.SCHEDULE_URL, timeout=5)
    r.raise_for_status()

    return r.json().get("scheduleChanges", [])


def format_lecture(lecture: Lecture) -> str:
    """Formats the given lecture according to the base template specified in messages."""
    return messages.LECTURE_BASE_TEMPLATE.format(
        time=lecture.date_time,
        discipline_name=lecture.discipline.name,
        event_type="Практика" if lecture.is_practice else "Лекция",
        cabinet=lecture.cabinet,
    )


def format_lecture_verbose(lecture: Lecture) -> str:
    """Formats the given lecture according to the verbose template specified in messages."""
    return messages.LECTURE_VERBOSE_TEMPLATE.format(
        time=lecture.date_time,
        discipline_name=lecture.discipline.name,
        event_type="Практика" if lecture.is_practice else "Лекция",
        cabinet=lecture.cabinet,
        teacher=lecture.teacher.fullname,
        age=lecture.teacher.age,
    )
