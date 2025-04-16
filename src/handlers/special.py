import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.config import settings
from src.utils import messages

logger = logging.getLogger(__name__)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /help command.
    Prints help message to the user.
    """
    if not update.effective_chat:
        logger.warning("Effective chat is None")
        return
    chat_id = update.effective_chat.id

    message = messages.HELP.format(
        update_time=settings.SCHEDULE_UPDATE_TIME,
        minutes_before=settings.MINUTES_BEFORE_LECTURE,
    )

    logger.info("User %s called the /help command", chat_id)
    await context.bot.send_message(chat_id=chat_id, text=message)


special_handlers = [CommandHandler("help", help)]
