import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository
from src.utils import global_utils, messages, schedule_utils

logger = logging.getLogger(__name__)


async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /next command.
    Fetches the nearest lecture and prints it to the user.
    Works both for subscribed and unsubscribed users.
    """
    if update.effective_chat is None:
        logger.warning("Effective chat is None")
        return
    chat_id = update.effective_chat.id

    logger.info("User %s requested the next lecture", chat_id)

    async with await get_session() as session:
        repo = ScheduleRepository(session)

        now = global_utils.get_local_now()
        next_lecture = await repo.get_next_lecture_after(now)

    message = schedule_utils.format_lecture_verbose(next_lecture) if next_lecture else messages.NO_NEXT_LECTURE
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")


schedule_handlers = [CommandHandler("next", next)]
