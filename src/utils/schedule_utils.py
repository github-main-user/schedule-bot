from collections import defaultdict
from typing import Sequence

from src.models.schedule import Lecture

from . import messages


def format_lecture(lecture: Lecture) -> str:
    """Formats given lecture according to the base template specified in messages."""

    return messages.LECTURE_BASE_TEMPLATE.format(
        time=lecture.starts_at,
        discipline_name=lecture.discipline.name,
        event_type="Практика" if lecture.is_practice else "Лекция",
        cabinet=lecture.cabinet,
    )


def format_lecture_verbose(lecture: Lecture) -> str:
    """Formats given lecture according to the verbose template specified in messages."""

    return messages.LECTURE_VERBOSE_TEMPLATE.format(
        time=lecture.starts_at,
        discipline_name=lecture.discipline.name,
        event_type="Практика" if lecture.is_practice else "Лекция",
        cabinet=lecture.cabinet,
        teacher=lecture.teacher.fullname,
        age=lecture.teacher.age,
    )


def format_lectures_by_their_dates(lectures: Sequence[Lecture]) -> str:
    """
    Formats given lectures, combine them by their dates.

    Example:
    =======

    DATE1
    lecture1
    lecture2

    DATE2
    lecture1
    lecture2
    lecture3
    """

    date_to_lectures_map = defaultdict(list)

    for lecture in lectures:
        date_to_lectures_map[lecture.starts_at.date()].append(lecture)

    return "\n\n".join(
        [
            messages.DATE_TEMPLATE.format(date=date)
            + "\n"
            + "\n".join(map(format_lecture, lectures))
            for date, lectures in date_to_lectures_map.items()
        ]
    )
