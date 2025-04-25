import logging
from functools import wraps
from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def with_chat_id(func: Callable) -> Callable:
    """
    Decorator for Telegram command handlers that extracts the chat ID from the update,
    logs the command usage, and passes the chat ID to the wrapped handler.
    """

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_chat:
            logger.warning("Effective chat is None")
            return

        chat_id = update.effective_chat.id
        logger.info("User %s called /%s", chat_id, func.__name__)
        await func(chat_id, update, context)

    return wrapper
