from src.models.schedule import Lecture

from . import messages


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
