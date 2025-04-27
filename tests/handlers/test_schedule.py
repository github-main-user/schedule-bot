from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.handlers.schedule import next
from src.models.schedule import Lecture


@pytest.fixture
def mock_get_session():
    with patch("src.handlers.schedule.get_session", autospec=True) as mock_get_session:
        yield mock_get_session


@pytest.fixture
def mock_schedule_repo():
    with patch(
        "src.handlers.schedule.ScheduleRepository", autospec=True
    ) as mock_schedule_repo:
        yield mock_schedule_repo


@pytest.mark.asyncio
async def test_next_empty_effective_chat(
    mock_get_session: AsyncMock, mock_update: MagicMock, mock_context: MagicMock
) -> None:
    mock_update.effective_chat = None

    await next(mock_update, mock_context)

    mock_get_session.assert_not_awaited()
    mock_context.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_next_success(
    mock_get_session: AsyncMock,
    mock_schedule_repo: MagicMock,
    mock_update: MagicMock,
    mock_context: MagicMock,
    lecture: Lecture,
) -> None:
    mock_schedule_repo.return_value.get_next_lecture_after = AsyncMock(
        return_value=lecture
    )

    await next(mock_update, mock_context)

    mock_get_session.assert_awaited_once()
    mock_schedule_repo.assert_called_once_with(
        mock_get_session.return_value.__aenter__.return_value
    )
    mock_schedule_repo.return_value.get_next_lecture_after.assert_awaited_once()
    mock_context.bot.send_message.assert_awaited_once()
