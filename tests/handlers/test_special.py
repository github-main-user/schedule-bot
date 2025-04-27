from unittest.mock import MagicMock

import pytest

from src.handlers.special import help


@pytest.mark.asyncio
async def test_help_no_effective_chat(
    mock_update: MagicMock, mock_context: MagicMock
) -> None:
    mock_update.effective_chat = None

    await help(mock_update, mock_context)

    mock_context.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_help_success(mock_update: MagicMock, mock_context: MagicMock) -> None:

    await help(mock_update, mock_context)

    mock_context.bot.send_message.assert_called_once()
