import logging
from datetime import date

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.db import get_session
from src.repositories.schedule_repository import ScheduleRepository
from src.utils import global_utils, messages, schedule_utils
from src.utils.bot_utils import with_chat_id

logger = logging.getLogger(__name__)


@with_chat_id
async def next(
    chat_id: int, _update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles /next command.
    Fetches the nearest lecture and prints it to user.
    Works both for subscribed and unsubscribed users.
    """

    async with await get_session() as session:
        repo = ScheduleRepository(session)

        now = global_utils.get_local_now()
        next_lecture = await repo.get_next_lecture_after(now)

        message = (
            f"{messages.DATE_TEMPLATE.format(date=next_lecture.starts_at)}"
            "\n"
            f"{schedule_utils.format_lecture_verbose(next_lecture)}"
            if next_lecture
            else messages.NO_NEXT_LECTURE
        )

    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")


@with_chat_id
async def today(
    chat_id: int, _update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles /today command.
    Fetches the today lectures and prints it to user.
    Works both for subscribed and unsubscribed users.
    """

    async with await get_session() as session:
        repo = ScheduleRepository(session)

        today_date = global_utils.get_local_today()
        today_lectures = await repo.get_lectures_for_day(today_date)

        message = (
            schedule_utils.format_lectures_by_their_dates(today_lectures)
            if today_lectures
            else messages.EMPTY_TODAY
        )

    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")


@with_chat_id
async def tomorrow(
    chat_id: int, _update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles /tomorrow command.
    Fetches the today lectures and prints it to user.
    Works both for subscribed and unsubscribed users.
    """

    async with await get_session() as session:
        repo = ScheduleRepository(session)

        tomorrow_date = global_utils.get_local_tomorrow()
        tomorrow_lectures = await repo.get_lectures_for_day(tomorrow_date)

        message = (
            schedule_utils.format_lectures_by_their_dates(tomorrow_lectures)
            if tomorrow_lectures
            else messages.EMPTY_TOMORROW
        )

    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")


schedule_handlers = [
    CommandHandler("next", next),
    CommandHandler("today", today),
    CommandHandler("tomorrow", tomorrow),
]
