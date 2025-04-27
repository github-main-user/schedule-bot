from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.handlers.subscribers import start, stop


@pytest.fixture
def mock_get_session():
    with patch(
        "src.handlers.subscribers.get_session", autospec=True
    ) as mock_get_session:
        yield mock_get_session


@pytest.fixture
def mock_subscriber_repo():
    with patch(
        "src.handlers.subscribers.SubscriberRepository", autospec=True
    ) as mock_subscriber_repo:
        yield mock_subscriber_repo


# =====
# start
# =====


@pytest.mark.asyncio
async def test_start_empty_effective_chat(
    mock_get_session: AsyncMock, mock_update: MagicMock, mock_context: MagicMock
) -> None:
    mock_update.effective_chat = None

    await start(mock_update, mock_context)

    mock_get_session.assert_not_awaited()
    mock_context.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_start_successfuly_subscribed(
    mock_get_session: AsyncMock,
    mock_subscriber_repo: MagicMock,
    mock_update: MagicMock,
    mock_context: MagicMock,
) -> None:
    mock_subscriber_repo.return_value.exists = AsyncMock(return_value=False)
    mock_subscriber_repo.return_value.create = AsyncMock()

    await start(mock_update, mock_context)

    mock_get_session.assert_awaited_once()
    mock_subscriber_repo.assert_called_once_with(
        mock_get_session.return_value.__aenter__.return_value
    )
    mock_subscriber_repo.return_value.exists.assert_awaited_once_with(
        mock_update.effective_chat.id
    )
    mock_subscriber_repo.return_value.create.assert_awaited_once_with(
        mock_update.effective_chat.id
    )
    mock_context.bot.send_message.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_already_subscribed(
    mock_get_session: AsyncMock,
    mock_subscriber_repo: MagicMock,
    mock_update: MagicMock,
    mock_context: MagicMock,
) -> None:
    mock_subscriber_repo.return_value.exists = AsyncMock(return_value=True)
    mock_subscriber_repo.return_value.create = AsyncMock()

    await start(mock_update, mock_context)

    mock_get_session.assert_awaited_once()
    mock_subscriber_repo.assert_called_once_with(
        mock_get_session.return_value.__aenter__.return_value
    )
    mock_subscriber_repo.return_value.exists.assert_awaited_once_with(
        mock_update.effective_chat.id
    )
    mock_subscriber_repo.return_value.create.assert_not_awaited()
    mock_context.bot.send_message.assert_awaited_once()


# ====
# stop
# ====


@pytest.mark.asyncio
async def test_stop_empty_effective_chat(
    mock_get_session: AsyncMock, mock_update: MagicMock, mock_context: MagicMock
) -> None:
    mock_update.effective_chat = None

    await stop(mock_update, mock_context)

    mock_get_session.assert_not_awaited()
    mock_context.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_stop_successfuly_subscribed(
    mock_get_session: AsyncMock,
    mock_subscriber_repo: MagicMock,
    mock_update: MagicMock,
    mock_context: MagicMock,
) -> None:
    mock_subscriber_repo.return_value.exists = AsyncMock(return_value=True)
    mock_subscriber_repo.return_value.delete = AsyncMock()

    await stop(mock_update, mock_context)

    mock_get_session.assert_awaited_once()
    mock_subscriber_repo.assert_called_once_with(
        mock_get_session.return_value.__aenter__.return_value
    )
    mock_subscriber_repo.return_value.exists.assert_awaited_once_with(
        mock_update.effective_chat.id
    )
    mock_subscriber_repo.return_value.delete.assert_awaited_once_with(
        mock_update.effective_chat.id
    )
    mock_context.bot.send_message.assert_awaited_once()


@pytest.mark.asyncio
async def test_stop_already_subscribed(
    mock_get_session: AsyncMock,
    mock_subscriber_repo: MagicMock,
    mock_update: MagicMock,
    mock_context: MagicMock,
) -> None:
    mock_subscriber_repo.return_value.exists = AsyncMock(return_value=False)
    mock_subscriber_repo.return_value.delete = AsyncMock()

    await stop(mock_update, mock_context)

    mock_get_session.assert_awaited_once()
    mock_subscriber_repo.assert_called_once_with(
        mock_get_session.return_value.__aenter__.return_value
    )
    mock_subscriber_repo.return_value.exists.assert_awaited_once_with(
        mock_update.effective_chat.id
    )
    mock_subscriber_repo.return_value.delete.assert_not_awaited()
    mock_context.bot.send_message.assert_awaited_once()
