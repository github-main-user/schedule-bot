from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.models.schedule import Discipline, Lecture, Teacher
from src.models.subscribers import Subscriber
from src.repositories.schedule_repository import ScheduleRepository
from src.repositories.subscriber_repository import SubscriberRepository

# Context


@pytest.fixture
def mock_context() -> MagicMock:
    context = MagicMock()
    context.bot.send_message = AsyncMock()
    return context


# Models


@pytest.fixture
def subscribers() -> list[Subscriber]:
    return [
        Subscriber(id=1, chat_id=112233),
        Subscriber(id=2, chat_id=223344),
        Subscriber(id=3, chat_id=334455),
    ]


@pytest.fixture
def subscriber(subscribers: list[Subscriber]) -> Subscriber:
    return subscribers[0]


@pytest.fixture
def lectures() -> list[Lecture]:
    discipline = Discipline(name="Test Discipline")
    teacher = Teacher(firstname="FirstName", lastname="LastName", patronymic="PatroNymic", birthday=date(1989, 11, 11))
    return [
        Lecture(
            id=1,
            starts_at=datetime(2025, 2, 12),
            discipline_id=1,
            teacher_id=1,
            cabinet="251",
            is_practice=True,
            teacher=teacher,
            discipline=discipline,
        ),
        Lecture(
            id=2,
            starts_at=datetime(2025, 2, 13),
            discipline_id=2,
            teacher_id=2,
            cabinet="252",
            is_practice=False,
            teacher=teacher,
            discipline=discipline,
        ),
        Lecture(
            id=3,
            starts_at=datetime(2025, 2, 14),
            discipline_id=3,
            teacher_id=3,
            cabinet="253",
            is_practice=True,
            teacher=teacher,
            discipline=discipline,
        ),
        Lecture(
            id=4,
            starts_at=datetime(2025, 2, 15),
            discipline_id=4,
            teacher_id=4,
            cabinet="254",
            is_practice=False,
            teacher=teacher,
            discipline=discipline,
        ),
    ]


@pytest.fixture
def lecture(lectures: list[Lecture]) -> Lecture:
    return lectures[0]
