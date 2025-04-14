from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository
from src.utils import global_utils, schedule_utils


async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /next command.
    Fetches the nearest lecture and prints it to the user.
    Works both for subscribed and unsubscribed users.
    """
    if update.effective_chat is None:
        return
    chat_id = update.effective_chat.id

    async with await get_session() as session:
        repo = ScheduleRepository(session)

        now = global_utils.get_local_now()
        next_lecture = await repo.get_next_lecture_after(now)
        if not next_lecture:
            return

    await context.bot.send_message(
        chat_id=chat_id,
        text=schedule_utils.format_lecture_verbose(next_lecture),
        parse_mode="Markdown",
    )


schedule_handlers = [CommandHandler("next", next)]
