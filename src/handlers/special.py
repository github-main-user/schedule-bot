import logging
import pprint

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.config import settings
from src.utils import messages
from src.utils.bot_utils import with_chat_id

logger = logging.getLogger(__name__)


@with_chat_id
async def help(chat_id: int, _update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /help command.
    Prints help message to the user.
    """

    message = messages.HELP.format(
        update_time=settings.SCHEDULE_UPDATE_TIME,
        minutes_before=settings.MINUTES_BEFORE_LECTURE,
    )

    await context.bot.send_message(chat_id=chat_id, text=message)


@with_chat_id
async def status(chat_id: int, _update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /status command.
    Prints currently active jobs to user.
    """

    jobs = context.job_queue.jobs() if context.job_queue else []

    await context.bot.send_message(chat_id=chat_id, text=pprint.pformat(jobs))


special_handlers = [
    CommandHandler("help", help),
    CommandHandler("status", status),
]
