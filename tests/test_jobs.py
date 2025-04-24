from datetime import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.jobs import daily_schedule_update, notify_about_upcoming_lecture
from src.models.schedule import Lecture
from src.models.subscribers import Subscriber

# ========
# fixtures
# ========


@pytest.fixture
def mock_update_schedule():
    with patch("src.jobs.update_schedule", autospec=True) as mock_update_schedule:
        yield mock_update_schedule


@pytest.fixture
def mock_get_session():
    with patch("src.jobs.get_session", autospec=True) as mock_get_session:
        yield mock_get_session


@pytest.fixture
def mock_schedule_repo():
    with patch("src.jobs.ScheduleRepository", autospec=True) as mock_schedule_repo:
        yield mock_schedule_repo


@pytest.fixture
def mock_subscriber_repo():
    with patch("src.jobs.SubscriberRepository", autospec=True) as mock_subscriber_repo:
        yield mock_subscriber_repo


# =====================
# daily_schedule_update
# =====================


@pytest.mark.asyncio
async def test_daily_schedule_update_with_lectures(
    mock_context: MagicMock,
    mock_schedule_repo: MagicMock,
    mock_subscriber_repo: MagicMock,
    mock_update_schedule: AsyncMock,
    mock_get_session: AsyncMock,
    lectures: list[Lecture],
    subscribers: list[Subscriber],
) -> None:
    # prepare
    session_obj = mock_get_session.return_value.__aenter__.return_value

    mock_schedule_repo.return_value.get_lectures_for_day = AsyncMock(return_value=lectures)
    mock_subscriber_repo.return_value.get_all = AsyncMock(return_value=subscribers)

    # actual call
    await daily_schedule_update(mock_context)

    # asserts
    mock_update_schedule.assert_awaited_once()

    mock_get_session.assert_awaited_once()
    mock_schedule_repo.assert_called_once_with(session_obj)
    mock_subscriber_repo.assert_called_once_with(session_obj)

    mock_schedule_repo.return_value.get_lectures_for_day.assert_awaited_once()
    mock_subscriber_repo.return_value.get_all.assert_awaited_once()

    assert (
        mock_context.bot.send_message.call_count == len(subscribers) * 2
    )  # * 2 because: "tomorrow next lectures" + "lectures itself"


@pytest.mark.asyncio
async def test_daily_schedule_update_wihtout_lectures(
    mock_context: MagicMock,
    mock_schedule_repo: MagicMock,
    mock_subscriber_repo: MagicMock,
    mock_update_schedule: AsyncMock,
    mock_get_session: AsyncMock,
    subscribers: list[Subscriber],
) -> None:
    # prepare
    session_obj = mock_get_session.return_value.__aenter__.return_value

    mock_schedule_repo.return_value.get_lectures_for_day = AsyncMock(return_value=[])
    mock_subscriber_repo.return_value.get_all = AsyncMock(return_value=subscribers)

    # actual call
    await daily_schedule_update(mock_context)

    # asserts
    mock_update_schedule.assert_awaited_once()

    mock_get_session.assert_awaited_once()
    mock_schedule_repo.assert_called_once_with(session_obj)
    mock_subscriber_repo.assert_called_once_with(session_obj)

    mock_schedule_repo.return_value.get_lectures_for_day.assert_awaited_once()
    mock_subscriber_repo.return_value.get_all.assert_awaited_once()

    assert mock_context.bot.send_message.call_count == len(subscribers)


@pytest.mark.asyncio
async def test_daily_schedule_update_without_subscribers(
    mock_context: MagicMock,
    mock_schedule_repo: MagicMock,
    mock_subscriber_repo: MagicMock,
    mock_update_schedule: AsyncMock,
    mock_get_session: AsyncMock,
    lectures: list[Lecture],
) -> None:
    # prepare
    session_obj = mock_get_session.return_value.__aenter__.return_value

    mock_schedule_repo.return_value.get_lectures_for_day = AsyncMock(return_value=lectures)
    mock_subscriber_repo.return_value.get_all = AsyncMock()

    # actual call
    await daily_schedule_update(mock_context)

    # asserts
    mock_update_schedule.assert_awaited_once()

    mock_get_session.assert_awaited_once()
    mock_schedule_repo.assert_called_once_with(session_obj)
    mock_subscriber_repo.assert_called_once_with(session_obj)

    mock_schedule_repo.return_value.get_lectures_for_day.assert_awaited_once()
    mock_subscriber_repo.return_value.get_all.assert_awaited_once()

    mock_context.bot.send_message.assert_not_called()


# =============================
# notify_about_upcoming_lecture
# =============================


@pytest.mark.asyncio
async def test_notify_about_upcoming_lecture_job_is_none(
    mock_context: MagicMock,
    mock_schedule_repo: MagicMock,
    mock_subscriber_repo: MagicMock,
    mock_get_session: AsyncMock,
) -> None:
    # prepare
    mock_context.job = None

    # actual call
    await notify_about_upcoming_lecture(mock_context)

    # asserts
    mock_get_session.assert_not_awaited()
    mock_schedule_repo.assert_not_called()
    mock_subscriber_repo.assert_not_called()


@pytest.mark.asyncio
async def test_notify_about_upcoming_lecture_success(
    mock_context: MagicMock,
    mock_schedule_repo: MagicMock,
    mock_subscriber_repo: MagicMock,
    mock_get_session: AsyncMock,
    lecture: Lecture,
    subscribers: list[Subscriber],
) -> None:
    # prepare
    session_obj = mock_get_session.return_value.__aenter__.return_value

    mock_context.job = MagicMock()
    mock_context.job.data = {"original_time": time(15, 30)}

    mock_schedule_repo.return_value.get_lecture_by_datetime = AsyncMock(return_value=lecture)
    mock_subscriber_repo.return_value.get_all = AsyncMock(return_value=subscribers)

    # actual call
    await notify_about_upcoming_lecture(mock_context)

    # asserts
    mock_get_session.assert_awaited_once()
    mock_schedule_repo.assert_called_once_with(session_obj)
    mock_subscriber_repo.assert_called_once_with(session_obj)

    mock_schedule_repo.return_value.get_lecture_by_datetime.assert_awaited_once()
    assert mock_context.bot.send_message.call_count == len(subscribers)


@pytest.mark.asyncio
async def test_notify_about_upcoming_lecture_no_next(
    mock_context: MagicMock,
    mock_schedule_repo: MagicMock,
    mock_subscriber_repo: MagicMock,
    mock_get_session: AsyncMock,
    subscribers: list[Subscriber],
) -> None:
    # prepare
    session_obj = mock_get_session.return_value.__aenter__.return_value

    mock_context.job = MagicMock()
    mock_context.job.data = {"original_time": time(15, 30)}

    mock_schedule_repo.return_value.get_lecture_by_datetime = AsyncMock(return_value=None)
    mock_subscriber_repo.return_value.get_all = AsyncMock(return_value=subscribers)

    # actual call
    await notify_about_upcoming_lecture(mock_context)

    # asserts
    mock_get_session.assert_awaited_once()
    mock_schedule_repo.assert_called_once_with(session_obj)
    mock_subscriber_repo.assert_called_once_with(session_obj)

    mock_schedule_repo.return_value.get_lecture_by_datetime.assert_awaited_once()
    mock_subscriber_repo.return_value.get_all.assert_not_awaited()
    mock_context.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_notify_about_upcoming_lecture_no_subscribers(
    mock_context: MagicMock,
    mock_schedule_repo: MagicMock,
    mock_subscriber_repo: MagicMock,
    mock_get_session: AsyncMock,
    lecture: Lecture,
) -> None:
    # prepare
    session_obj = mock_get_session.return_value.__aenter__.return_value

    mock_context.job = MagicMock()
    mock_context.job.data = {"original_time": time(15, 30)}

    mock_schedule_repo.return_value.get_lecture_by_datetime = AsyncMock(return_value=lecture)
    mock_subscriber_repo.return_value.get_all = AsyncMock(return_value=[])

    # actual call
    await notify_about_upcoming_lecture(mock_context)

    # asserts
    mock_get_session.assert_awaited_once()
    mock_schedule_repo.assert_called_once_with(session_obj)
    mock_subscriber_repo.assert_called_once_with(session_obj)

    mock_schedule_repo.return_value.get_lecture_by_datetime.assert_awaited_once()
    mock_context.bot.send_message.assert_not_awaited()
